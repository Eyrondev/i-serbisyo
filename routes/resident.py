from flask import render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from . import resident_bp
from models import db, Resident, Certificate, Announcement, User, CertificateType
from utils import resident_required, get_current_user
from datetime import datetime, timedelta

@resident_bp.route('/dashboard')
@resident_required
def dashboard():
    # Get current user and resident's profile
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    # Get resident's certificates with status counts
    certificates = Certificate.query.filter_by(resident_id=resident.id).all()
    
    # Calculate certificate statistics
    cert_stats = {
        'total': len(certificates),
        'pending': len([c for c in certificates if c.status == 'pending']),
        'approved': len([c for c in certificates if c.status in ['completed', 'ready', 'claimed']]),
        'processing': len([c for c in certificates if c.status == 'processing']),
        'rejected': len([c for c in certificates if c.status == 'rejected'])
    }
    
    # Get recent certificates (last 5)
    recent_certificates = Certificate.query.filter_by(resident_id=resident.id)\
        .order_by(Certificate.request_date.desc()).limit(5).all()
    
    # Get recent announcements (latest 3 published announcements that are not expired)
    current_time = datetime.utcnow()
    recent_announcements = Announcement.query.filter(
        Announcement.status == 'published'
    ).filter(
        db.or_(
            Announcement.expiry_date.is_(None),
            Announcement.expiry_date > current_time
        )
    ).order_by(Announcement.created_at.desc()).limit(3).all()
    
    # Get announcement count for this week (non-expired only)
    week_ago = datetime.now() - timedelta(days=7)
    announcement_count = Announcement.query.filter(
        Announcement.status == 'published',
        Announcement.created_at >= week_ago
    ).filter(
        db.or_(
            Announcement.expiry_date.is_(None),
            Announcement.expiry_date > current_time
        )
    ).count()
    
    # Prepare dashboard statistics
    dashboard_stats = {
        'certificates': cert_stats,
        'announcements': announcement_count,
        'resident_status': resident.status,
        'is_voter': resident.is_voter
    }
    
    return render_template('residents/dashboard.html', 
                         resident=resident, 
                         certificates=certificates,
                         recent_certificates=recent_certificates,
                         recent_announcements=recent_announcements,
                         dashboard_stats=dashboard_stats,
                         current_user=current_user)

@resident_bp.route('/certificates')
@resident_required
def certificates():
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    # Get filter parameters
    search_query = request.args.get('search', '').strip()
    certificate_type = request.args.get('type', '')
    status_filter = request.args.get('status', '')
    
    # Build query
    query = Certificate.query.filter_by(resident_id=resident.id)
    
    # Apply filters
    if search_query:
        query = query.filter(Certificate.certificate_type.ilike(f'%{search_query}%'))
    
    if certificate_type:
        query = query.filter(Certificate.certificate_type == certificate_type)
    
    if status_filter:
        query = query.filter(Certificate.status == status_filter)
    
    # Get filtered certificates
    certificates = query.order_by(Certificate.request_date.desc()).all()
    
    # Calculate statistics
    all_certificates = Certificate.query.filter_by(resident_id=resident.id).all()
    cert_stats = {
        'total': len(all_certificates),
        'pending': len([c for c in all_certificates if c.status == 'pending']),
        'approved': len([c for c in all_certificates if c.status in ['completed', 'ready', 'claimed']]),
        'processing': len([c for c in all_certificates if c.status == 'processing']),
        'ready': len([c for c in all_certificates if c.status == 'ready']),
        'cancelled': len([c for c in all_certificates if c.status == 'cancelled'])
    }
    
    # Get unique certificate types for filter dropdown
    certificate_types = list(set([cert.certificate_type for cert in all_certificates]))
    
    # Get available certificate types from database for new requests
    available_cert_types = CertificateType.query.filter_by(
        is_active=True,
        is_available_online=True
    ).order_by(CertificateType.name).all()
    
    return render_template('residents/certificates.html', 
                         certificates=certificates,
                         cert_stats=cert_stats,
                         certificate_types=certificate_types,
                         available_cert_types=available_cert_types,
                         search_query=search_query,
                         certificate_type=certificate_type,
                         status_filter=status_filter,
                         current_user=current_user)

@resident_bp.route('/announcements')
@resident_required
def announcements():
    current_user = get_current_user()
    
    # Get filter parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '')
    sort_order = request.args.get('sort', 'latest')
    
    # Build query - filter published announcements that are not expired
    query = Announcement.query.filter_by(status='published')
    
    # Filter out expired announcements
    # Show announcements with no expiry date OR expiry date in the future
    current_time = datetime.utcnow()
    query = query.filter(
        db.or_(
            Announcement.expiry_date.is_(None),
            Announcement.expiry_date > current_time
        )
    )
    
    # Apply filters
    if search_query:
        query = query.filter(
            db.or_(
                Announcement.title.ilike(f'%{search_query}%'),
                Announcement.content.ilike(f'%{search_query}%')
            )
        )
    
    if category_filter:
        query = query.filter(Announcement.category == category_filter)
    
    # Apply sorting
    if sort_order == 'oldest':
        query = query.order_by(Announcement.created_at.asc())
    elif sort_order == 'priority':
        # Order by priority: urgent, high, medium, low
        priority_order = db.case(
            (Announcement.priority == 'urgent', 1),
            (Announcement.priority == 'high', 2),
            (Announcement.priority == 'medium', 3),
            (Announcement.priority == 'low', 4),
            else_=5
        )
        query = query.order_by(priority_order, Announcement.created_at.desc())
    else:  # latest first (default)
        query = query.order_by(Announcement.created_at.desc())
    
    # Get announcements
    announcements = query.all()
    
    # Get all non-expired published announcements for category dropdown
    # (without search/category filters applied)
    all_non_expired = Announcement.query.filter_by(status='published').filter(
        db.or_(
            Announcement.expiry_date.is_(None),
            Announcement.expiry_date > current_time
        )
    ).all()
    categories = list(set([ann.category for ann in all_non_expired if ann.category]))
    
    # Count announcements by priority - ONLY from filtered/displayed announcements
    # This ensures stats match what user actually sees
    announcement_stats = {
        'total': len(announcements),
        'urgent': len([a for a in announcements if a.priority == 'urgent']),
        'high': len([a for a in announcements if a.priority == 'high']),
        'medium': len([a for a in announcements if a.priority == 'medium']),
        'low': len([a for a in announcements if a.priority == 'low']),
        'active': len(announcements)  # Active = currently displayed (non-expired + filters applied)
    }
    
    return render_template('residents/announcements.html',
                         announcements=announcements,
                         categories=categories,
                         announcement_stats=announcement_stats,
                         search_query=search_query,
                         category_filter=category_filter,
                         sort_order=sort_order,
                         current_user=current_user)

@resident_bp.route('/certificate/request', methods=['POST'])
@resident_required
def request_certificate():
    """Handle new certificate requests"""
    from datetime import datetime
    
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Get form data
    certificate_type = request.form.get('certificate_type', '').strip()
    purpose = request.form.get('purpose', '').strip()
    other_purpose = request.form.get('other_purpose', '').strip()
    notes = request.form.get('notes', '').strip()
    
    # Debug logging
    print(f"\n{'='*60}")
    print(f"NEW CERTIFICATE REQUEST FROM RESIDENT ID: {resident.id}")
    print(f"Certificate Type Code: {certificate_type}")
    print(f"Purpose: {purpose}")
    print(f"Other Purpose: {other_purpose}")
    print(f"Notes: {notes}")
    print(f"{'='*60}\n")
    
    # Validation
    if not certificate_type:
        flash('Please select a certificate type.', 'error')
        return redirect(url_for('resident.certificates'))
    
    if not purpose:
        flash('Please select a purpose.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Handle "other" purpose
    final_purpose = other_purpose if purpose == 'other' and other_purpose else purpose
    
    if not final_purpose:
        flash('Please specify the purpose for your certificate request.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Get certificate type details from database
    cert_type = CertificateType.query.filter_by(code=certificate_type, is_active=True).first()
    
    if not cert_type:
        print(f"❌ ERROR: Certificate type '{certificate_type}' not found in database!")
        flash('Invalid certificate type selected.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Use certificate type name and fee from database
    certificate_name = cert_type.name
    certificate_fee = float(cert_type.fee)
    
    print(f"✅ Certificate Type Found: {certificate_name} (Fee: ₱{certificate_fee})")
    
    try:
        # Create new certificate request
        new_certificate = Certificate(
            resident_id=resident.id,
            certificate_type=certificate_name,
            purpose=final_purpose,
            notes=notes if notes else None,
            status='pending',
            request_date=datetime.now(),
            fee=certificate_fee
        )
        
        db.session.add(new_certificate)
        db.session.commit()
        
        print(f"✅ Certificate Request Created Successfully! ID: {new_certificate.id}")
        print(f"{'='*60}\n")
        
        print(f"✅ Certificate Request Created Successfully! ID: {new_certificate.id}")
        print(f"{'='*60}\n")
        
        flash(f'Certificate request submitted successfully! Your request ID is REQ-{new_certificate.id}-{new_certificate.request_date.year}. You will be notified once it\'s ready for pickup.', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR Creating Certificate: {str(e)}")
        print(f"{'='*60}\n")
        flash('Error submitting certificate request. Please try again.', 'error')
    
    return redirect(url_for('resident.certificates'))

@resident_bp.route('/certificate/<int:certificate_id>/view')
@resident_required
def view_certificate(certificate_id):
    """View certificate details (placeholder for future implementation)"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    # Verify certificate belongs to current resident
    certificate = Certificate.query.filter_by(id=certificate_id, resident_id=resident.id).first()
    
    if not certificate:
        flash('Certificate not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # This would render a detailed certificate view
    flash(f'Viewing details for {certificate.certificate_type} certificate.', 'info')
    return redirect(url_for('resident.certificates'))

@resident_bp.route('/certificate/<int:certificate_id>/cancel', methods=['POST'])
@resident_required
def cancel_certificate(certificate_id):
    """Cancel a pending certificate request"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Verify certificate belongs to current resident
    certificate = Certificate.query.filter_by(id=certificate_id, resident_id=resident.id).first()
    
    if not certificate:
        flash('Certificate not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Only allow cancellation of pending requests
    if certificate.status != 'pending':
        flash('Only pending certificate requests can be cancelled.', 'error')
        return redirect(url_for('resident.certificates'))
    
    try:
        # Update certificate status to cancelled
        certificate.status = 'cancelled'
        certificate.processed_date = datetime.now()
        certificate.rejection_reason = 'Cancelled by resident'
        
        db.session.commit()
        flash(f'Certificate request for {certificate.certificate_type} has been cancelled successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Error cancelling certificate request. Please try again.', 'error')
        print(f"Error cancelling certificate: {e}")
    
    return redirect(url_for('resident.certificates'))

@resident_bp.route('/certificate/<int:certificate_id>/edit', methods=['GET', 'POST'])
@resident_required
def edit_certificate(certificate_id):
    """Edit a pending certificate request"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Verify certificate belongs to current resident
    certificate = Certificate.query.filter_by(id=certificate_id, resident_id=resident.id).first()
    
    if not certificate:
        flash('Certificate not found.', 'error')
        return redirect(url_for('resident.certificates'))
    
    # Only allow editing of pending requests
    if certificate.status != 'pending':
        flash('Only pending certificate requests can be edited.', 'error')
        return redirect(url_for('resident.certificates'))
    
    if request.method == 'POST':
        # Handle form submission for editing
        purpose = request.form.get('purpose', '').strip()
        other_purpose = request.form.get('other_purpose', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if not purpose:
            flash('Please select a purpose.', 'error')
            return redirect(url_for('resident.certificates'))
        
        # Handle "other" purpose
        final_purpose = other_purpose if purpose == 'other' and other_purpose else purpose
        
        if not final_purpose:
            flash('Please specify the purpose for your certificate request.', 'error')
            return redirect(url_for('resident.certificates'))
        
        try:
            # Update certificate details
            certificate.purpose = final_purpose
            certificate.notes = notes if notes else None
            
            db.session.commit()
            flash(f'Certificate request for {certificate.certificate_type} has been updated successfully.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating certificate request. Please try again.', 'error')
            print(f"Error updating certificate: {e}")
        
        return redirect(url_for('resident.certificates'))
    
    # For GET request, this would render an edit form
    # For now, just redirect back with info message
    flash(f'Edit functionality for {certificate.certificate_type} certificate would be implemented here.', 'info')
    return redirect(url_for('resident.certificates'))

@resident_bp.route('/profile')
@resident_required
def profile():
    """Display resident profile page"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.dashboard'))
    
    return render_template('residents/profile.html', 
                         current_user=current_user, 
                         resident=resident)

@resident_bp.route('/profile/edit', methods=['GET', 'POST'])
@resident_required
def edit_profile():
    """Edit resident profile"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.dashboard'))
    
    if request.method == 'POST':
        try:
            # Update user information
            current_user.name = request.form.get('name', '').strip()
            current_user.email = request.form.get('email', '').strip()
            
            # Update resident information
            resident.first_name = request.form.get('first_name', '').strip()
            resident.middle_name = request.form.get('middle_name', '').strip()
            resident.last_name = request.form.get('last_name', '').strip()
            resident.suffix = request.form.get('suffix', '').strip()
            resident.phone = request.form.get('phone', '').strip()
            resident.house_number = request.form.get('house_number', '').strip()
            resident.street = request.form.get('street', '').strip()
            resident.purok = request.form.get('purok', '').strip()
            resident.gender = request.form.get('gender', '').strip()
            resident.civil_status = request.form.get('civil_status', '').strip()
            resident.occupation = request.form.get('occupation', '').strip()
            
            # Handle birth date
            birth_date_str = request.form.get('birth_date')
            if birth_date_str:
                try:
                    resident.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Invalid birth date format.', 'error')
                    return redirect(url_for('resident.edit_profile'))
            
            resident.birth_place = request.form.get('birth_place', '').strip()
            
            # Update timestamps
            current_user.updated_at = datetime.utcnow()
            resident.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('resident.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')
            print(f"Error updating profile: {e}")
            return redirect(url_for('resident.edit_profile'))
    
    return render_template('residents/edit-profile.html', 
                         current_user=current_user, 
                         resident=resident)

@resident_bp.route('/settings')
@resident_required
def settings():
    """Display resident settings page"""
    current_user = get_current_user()
    resident = Resident.query.filter_by(user_id=session['user']['id']).first()
    
    if not resident:
        flash('Resident profile not found.', 'error')
        return redirect(url_for('resident.dashboard'))
    
    return render_template('residents/settings.html', 
                         current_user=current_user, 
                         resident=resident)

@resident_bp.route('/settings/password', methods=['POST'])
@resident_required
def change_password():
    """Change user password"""
    current_user = get_current_user()
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_password or not new_password or not confirm_password:
        flash('All password fields are required.', 'error')
        return redirect(url_for('resident.settings'))
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('resident.settings'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('resident.settings'))
    
    if len(new_password) < 6:
        flash('New password must be at least 6 characters long.', 'error')
        return redirect(url_for('resident.settings'))
    
    try:
        current_user.set_password(new_password)
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Password changed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error changing password. Please try again.', 'error')
        print(f"Error changing password: {e}")
    
    return redirect(url_for('resident.settings'))
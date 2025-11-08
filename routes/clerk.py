from flask import render_template, request, session, redirect, url_for, flash, jsonify
from . import clerk_bp
from models import db, User, Resident, Certificate, CertificateType, Official, Announcement, BlotterRecord, SystemActivity, Payment, SystemSettings, BarangayInfo, PurokInfo
from utils import clerk_required, success_response, error_response
from activity_logger import (log_resident_action, log_certificate_action, log_official_action, 
                             log_blotter_action, log_announcement_action, log_payment_action, ActivityTypes)
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import calendar
from decimal import Decimal
import os
import uuid
from werkzeug.utils import secure_filename

def get_notification_counts():
    """Get notification counts for admin sidebar"""
    try:
        # Pending residents count
        pending_residents = Resident.query.filter_by(status='pending').count()
        
        # Pending certificate requests count
        pending_certificates = Certificate.query.filter_by(status='pending').count()
        
        return {
            'pending_residents': pending_residents,
            'certificate_requests': pending_certificates
        }
    except Exception:
        # Return default values if database query fails
        return {
            'pending_residents': 0,
            'certificate_requests': 0
        }

# Add context processor to inject notification counts into all clerk templates
@clerk_bp.context_processor
def inject_notification_counts():
    """Inject notification counts into all clerk templates"""
    return {'notification_counts': get_notification_counts()}

def get_certificate_fees():
    """Get certificate fees from database, fallback to defaults if database is empty"""
    try:
        # Try to get fees from database first
        certificate_types = CertificateType.query.filter_by(is_active=True).all()
        
        if certificate_types:
            # Use database values
            fees = {}
            for cert_type in certificate_types:
                fees[cert_type.code] = cert_type.fee
            return fees
        else:
            # Fallback to default values if database is empty
            return {
                'barangay_clearance': Decimal('50.00'),
                'certificate_of_residency': Decimal('30.00'),
                'certificate_of_indigency': Decimal('25.00'),
                'business_permit': Decimal('200.00'),
                'health_certificate': Decimal('100.00'),
                'good_moral_character': Decimal('75.00')
            }
    except Exception as e:
        # Fallback to default values if database query fails
        print(f"Warning: Could not load certificate fees from database: {e}")
        return {
            'barangay_clearance': Decimal('50.00'),
            'certificate_of_residency': Decimal('30.00'),
            'certificate_of_indigency': Decimal('25.00'),
            'business_permit': Decimal('200.00'),
            'health_certificate': Decimal('100.00'),
            'good_moral_character': Decimal('75.00')
        }

def save_profile_picture(file):
    """Save uploaded profile picture and return filename"""
    if not file or file.filename == '':
        return None
    
    # Check if file is allowed
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return None
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Create uploads directory if it doesn't exist
    upload_folder = os.path.join('static', 'uploads', 'profiles')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    return unique_filename

@clerk_bp.route('/dashboard')
@clerk_required
def dashboard():
    # Get dashboard statistics
    total_residents = Resident.query.filter_by(status='approved').count()
    pending_requests = Certificate.query.filter_by(status='pending').count()
    pending_residents = Resident.query.filter_by(status='pending').count()
    
    # Calculate monthly revenue from paid certificates
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_revenue = db.session.query(func.sum(Certificate.fee)).filter(
        Certificate.payment_status == 'paid',
        extract('month', Certificate.payment_date) == current_month,
        extract('year', Certificate.payment_date) == current_year
    ).scalar() or Decimal('0.00')
    
    # Also calculate potential revenue from unpaid certificates
    certificate_fees = get_certificate_fees()
    unpaid_certificates = Certificate.query.filter_by(payment_status='unpaid').all()
    pending_revenue = sum([
        cert.fee or certificate_fees.get(cert.certificate_type, Decimal('0.00')) 
        for cert in unpaid_certificates
    ])
    
    # Calculate satisfaction rate (mock calculation based on approved vs total requests)
    total_requests = Certificate.query.count()
    completed_requests = Certificate.query.filter_by(status='claimed').count()
    satisfaction_rate = round((completed_requests / total_requests * 100) if total_requests > 0 else 100, 1)
    
    # Get recent activities
    recent_certificates = Certificate.query.join(Resident).order_by(
        # Prioritize active certificates in recent list too
        db.case(
            (db.and_(Certificate.status == 'completed', Certificate.payment_status == 'paid'), 3),
            (Certificate.status == 'completed', 2),
            (Certificate.status == 'rejected', 1),
            else_=0
        ),
        Certificate.request_date.desc()
    ).limit(5).all()
    recent_residents = Resident.query.filter_by(status='pending').order_by(Resident.created_at.desc()).limit(3).all()
    recent_approved = Resident.query.filter_by(status='approved').order_by(Resident.updated_at.desc()).limit(2).all()
    
    # Get monthly service requests (this month)
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_requests = Certificate.query.filter(Certificate.request_date >= month_start).count()
    
    # Get today's statistics
    today = datetime.now().date()
    certificates_today = Certificate.query.filter(
        db.func.date(Certificate.request_date) == today
    ).count()
    
    residents_approved_today = Resident.query.filter(
        Resident.status == 'approved',
        db.func.date(Resident.updated_at) == today
    ).count()
    
    # Get monthly data for chart (last 12 months)
    monthly_chart_data = []
    monthly_labels = []
    current_date = datetime.now()
    
    for i in range(11, -1, -1):  # Loop backwards from 11 months ago to current month
        # Calculate the target month and year
        target_month = current_date.month - i
        target_year = current_date.year
        
        # Handle year rollover
        while target_month <= 0:
            target_month += 12
            target_year -= 1
        
        # Get start and end of the target month
        month_start_date = datetime(target_year, target_month, 1)
        
        # Calculate next month for range
        next_month = target_month + 1
        next_year = target_year
        if next_month > 12:
            next_month = 1
            next_year += 1
        month_end_date = datetime(next_year, next_month, 1)
        
        # Count certificates for this month
        count = Certificate.query.filter(
            Certificate.request_date >= month_start_date,
            Certificate.request_date < month_end_date
        ).count()
        
        monthly_chart_data.append(count)
        monthly_labels.append(calendar.month_abbr[target_month])
    
    # Calculate percentage change (compare current month to previous month)
    if len(monthly_chart_data) >= 2:
        current_month_count = monthly_chart_data[-1]
        previous_month_count = monthly_chart_data[-2]
        if previous_month_count > 0:
            requests_change = round(((current_month_count - previous_month_count) / previous_month_count) * 100, 1)
        else:
            requests_change = 100 if current_month_count > 0 else 0
    else:
        requests_change = 0
    
    revenue_change = 12  # Mock percentage change for now
    
    stats = {
        'total_residents': total_residents,
        'pending_requests': pending_requests,  # Only certificate requests
        'monthly_revenue': float(monthly_revenue),
        'pending_revenue': float(pending_revenue),
        'satisfaction_rate': satisfaction_rate,
        'monthly_requests': monthly_requests,
        'revenue_change': revenue_change,
        'requests_change': requests_change,
        'certificates_pending': pending_requests,
        'residents_pending_approval': pending_residents,
        'certificates_today': certificates_today,
        'residents_approved_today': residents_approved_today,
        'monthly_chart_data': monthly_chart_data,
        'monthly_labels': monthly_labels
    }
    
    return render_template('clerk/dashboard.html', 
                         stats=stats,
                         recent_certificates=recent_certificates,
                         recent_residents=recent_residents,
                         recent_approved=recent_approved)

@clerk_bp.route('/residents')
@clerk_required
def residents():
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    age_filter = request.args.get('age', '')
    gender_filter = request.args.get('gender', '')
    status_filter = request.args.get('status', 'approved')  # Default to approved residents
    search_query = request.args.get('search', '')
    
    # Build base query
    query = Resident.query
    
    # Apply status filter (default to approved residents)
    if status_filter:
        query = query.filter_by(status=status_filter)
    else:
        query = query.filter_by(status='approved')
    
    # Apply gender filter
    if gender_filter:
        query = query.filter_by(gender=gender_filter)
    
    # Apply search filter
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Resident.first_name.ilike(search_term),
                Resident.last_name.ilike(search_term),
                Resident.email.ilike(search_term),
                Resident.phone.ilike(search_term),
                Resident.occupation.ilike(search_term)
            )
        )
    
    # Apply age filter (requires calculation based on birth_date)
    if age_filter:
        from datetime import date
        today = date.today()
        if age_filter == 'minor':
            # 0-17 years old
            birth_year_start = today.year - 17
            query = query.filter(extract('year', Resident.birth_date) > birth_year_start)
        elif age_filter == 'adult':
            # 18-59 years old
            birth_year_start = today.year - 59
            birth_year_end = today.year - 18
            query = query.filter(
                extract('year', Resident.birth_date) <= birth_year_end,
                extract('year', Resident.birth_date) > birth_year_start
            )
        elif age_filter == 'senior':
            # 60+ years old
            birth_year_end = today.year - 60
            query = query.filter(extract('year', Resident.birth_date) <= birth_year_end)
    
    # Get paginated results
    residents_paginated = query.order_by(Resident.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    # Calculate statistics
    all_approved = Resident.query.filter_by(status='approved')
    total_residents = all_approved.count()
    
    # Gender statistics
    male_count = all_approved.filter_by(gender='Male').count()
    female_count = all_approved.filter_by(gender='Female').count()
    
    # Age-based statistics
    from datetime import date
    today = date.today()
    
    # Senior citizens (60+)
    senior_count = all_approved.filter(
        extract('year', Resident.birth_date) <= today.year - 60
    ).count()
    
    # PWD count (this would need to be added to the model, for now using placeholder)
    pwd_count = 0  # Placeholder - would need PWD field in model
    
    stats = {
        'total_residents': total_residents,
        'male_count': male_count,
        'female_count': female_count,
        'senior_count': senior_count,
        'pwd_count': pwd_count
    }
    
    # Get all active sitios/puroks for the dropdown
    purok_list = PurokInfo.query.filter_by(is_active=True).order_by(PurokInfo.name).all()
    
    return render_template('clerk/residents.html', 
                         residents=residents_paginated, 
                         stats=stats,
                         purok_list=purok_list,
                         current_filters={
                             'age': age_filter,
                             'gender': gender_filter,
                             'status': status_filter,
                             'search': search_query
                         })

@clerk_bp.route('/pending-residents')
@clerk_required
def pending_residents():
    # Get filter parameters
    status_filter = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    # Build query with filters
    query = Resident.query.filter_by(status='pending')
    
    # Apply search filter
    if search_query:
        query = query.filter(
            db.or_(
                Resident.first_name.contains(search_query),
                Resident.last_name.contains(search_query),
                Resident.email.contains(search_query)
            )
        )
    
    # Apply date range filter
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Resident.created_at >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            # Add one day to include the entire end date
            to_date = to_date.replace(hour=23, minute=59, second=59)
            query = query.filter(Resident.created_at <= to_date)
        except ValueError:
            pass
    
    # Get paginated results
    residents = query.order_by(Resident.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Calculate statistics
    total_pending = Resident.query.filter_by(status='pending').count()
    
    # Approved today
    today = datetime.now().date()
    approved_today = Resident.query.filter(
        Resident.status == 'approved',
        db.func.date(Resident.updated_at) == today
    ).count()
    
    # Needs review (pending for more than 3 days)
    three_days_ago = datetime.now() - timedelta(days=3)
    needs_review = Resident.query.filter(
        Resident.status == 'pending',
        Resident.created_at <= three_days_ago
    ).count()
    
    # Rejected today
    rejected_today = Resident.query.filter(
        Resident.status == 'rejected',
        db.func.date(Resident.updated_at) == today
    ).count()
    
    stats = {
        'total_pending': total_pending,
        'approved_today': approved_today,
        'needs_review': needs_review,
        'rejected_today': rejected_today
    }
    
    # Current filters for template
    current_filters = {
        'status': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'search': search_query
    }
    
    return render_template('clerk/pending-residents.html', 
                         residents=residents,
                         stats=stats,
                         current_filters=current_filters)

@clerk_bp.route('/certificates')
@clerk_required
def certificates():
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Fixed to 10 items per page
    certificate_type = request.args.get('type', '')
    status_filter = request.args.get('status', '')
    search_query = request.args.get('search', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build base query with joins
    query = Certificate.query.join(Resident)
    
    # Apply certificate type filter
    if certificate_type:
        query = query.filter(Certificate.certificate_type == certificate_type)
    
    # Apply status filter
    if status_filter:
        query = query.filter(Certificate.status == status_filter)
    
    # Apply search filter
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Resident.first_name.ilike(search_term),
                Resident.last_name.ilike(search_term),
                Certificate.certificate_number.ilike(search_term),
                Certificate.purpose.ilike(search_term)
            )
        )
    
    # Apply date filters
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Certificate.request_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            from datetime import datetime, timedelta
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Certificate.request_date < date_to_obj)
        except ValueError:
            pass
    
    # Get paginated results with custom ordering to prioritize active certificates
    # Priority order: pending > processing > approved > ready > rejected > completed (with paid at the very bottom)
    certificates_paginated = query.order_by(
        # Primary sort: Prioritize active certificates over completed ones
        db.case(
            (db.and_(Certificate.status == 'completed', Certificate.payment_status == 'paid'), 3),  # Lowest priority
            (Certificate.status == 'completed', 2),  # Second lowest priority
            (Certificate.status == 'rejected', 1),   # Third lowest priority
            else_=0  # Highest priority for all active statuses
        ),
        # Secondary sort: Among same priority groups, sort by status importance
        db.case(
            (Certificate.status == 'pending', 0),
            (Certificate.status == 'processing', 1),
            (Certificate.status == 'approved', 2),
            (Certificate.status == 'ready', 3),
            (Certificate.status == 'rejected', 4),
            (Certificate.status == 'completed', 5),
            else_=6
        ),
        # Tertiary sort: Within same status, newest first
        Certificate.request_date.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Calculate statistics
    all_certificates = Certificate.query
    total_requests = all_certificates.count()
    pending_count = all_certificates.filter_by(status='pending').count()
    processing_count = all_certificates.filter_by(status='processing').count()
    approved_count = all_certificates.filter_by(status='approved').count()
    ready_count = all_certificates.filter_by(status='ready').count()
    completed_count = all_certificates.filter_by(status='completed').count()
    rejected_count = all_certificates.filter_by(status='rejected').count()
    
    # Certificate type statistics with percentages
    type_stats = db.session.query(
        Certificate.certificate_type,
        func.count(Certificate.id).label('count')
    ).group_by(Certificate.certificate_type).order_by(func.count(Certificate.id).desc()).all()
    
    # Calculate percentages for popular certificates
    certificate_type_names = {
        'barangay_clearance': 'Barangay Clearance',
        'certificate_of_indigency': 'Certificate of Indigency',
        'business_permit': 'Business Permit',
        'certificate_of_residency': 'Certificate of Residency',
        'cedula': 'Cedula',
        'tribal_membership': 'Tribal Membership'
    }
    
    popular_certificates = []
    for stat in type_stats:
        percentage = round((stat.count / total_requests * 100) if total_requests > 0 else 0, 1)
        popular_certificates.append({
            'type': stat.certificate_type,
            'type_name': certificate_type_names.get(stat.certificate_type, stat.certificate_type.replace('_', ' ').title()),
            'count': stat.count,
            'percentage': percentage
        })
    
    # Payment statistics
    paid_count = all_certificates.filter_by(payment_status='paid').count()
    unpaid_count = all_certificates.filter_by(payment_status='unpaid').count()
    total_revenue = db.session.query(func.sum(Certificate.fee)).filter_by(payment_status='paid').scalar() or 0
    
    stats = {
        'total_requests': total_requests,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'approved_count': approved_count,
        'ready_count': ready_count,
        'completed_count': completed_count,
        'rejected_count': rejected_count,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'total_revenue': float(total_revenue),
        'type_stats': {stat.certificate_type: stat.count for stat in type_stats},
        'popular_certificates': popular_certificates
    }
    
    # Handle export requests
    export_format = request.args.get('export')
    if export_format in ['excel', 'csv']:
        # Get all filtered results (not paginated) for export with same ordering as main view
        all_certificates_query = query.order_by(
            # Primary sort: Prioritize active certificates over completed ones
            db.case(
                (db.and_(Certificate.status == 'completed', Certificate.payment_status == 'paid'), 3),  # Lowest priority
                (Certificate.status == 'completed', 2),  # Second lowest priority
                (Certificate.status == 'rejected', 1),   # Third lowest priority
                else_=0  # Highest priority for all active statuses
            ),
            # Secondary sort: Among same priority groups, sort by status importance
            db.case(
                (Certificate.status == 'pending', 0),
                (Certificate.status == 'processing', 1),
                (Certificate.status == 'approved', 2),
                (Certificate.status == 'ready', 3),
                (Certificate.status == 'rejected', 4),
                (Certificate.status == 'completed', 5),
                else_=6
            ),
            # Tertiary sort: Within same status, newest first
            Certificate.request_date.desc()
        ).all()
        
        if export_format == 'csv':
            from flask import make_response
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(['Certificate Number', 'Resident Name', 'Certificate Type', 
                           'Purpose', 'Status', 'Payment Status', 'Fee', 'Request Date', 'Completion Date'])
            
            # Write data
            for cert in all_certificates_query:
                writer.writerow([
                    cert.certificate_number or f'CERT-{cert.id:04d}',
                    cert.resident.full_name,
                    certificate_type_names.get(cert.certificate_type, cert.certificate_type.replace('_', ' ').title()),
                    cert.purpose or 'Not specified',
                    cert.status.title(),
                    cert.payment_status.title(),
                    f'₱{cert.fee:.2f}',
                    cert.request_date.strftime('%Y-%m-%d') if cert.request_date else '',
                    cert.completion_date.strftime('%Y-%m-%d') if cert.completion_date else ''
                ])
            
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=certificates.csv'
            return response
            
        elif export_format == 'excel':
            # For now, return CSV format with Excel content type
            # You can implement proper Excel export using openpyxl later
            return render_template('clerk/certificates.html', 
                                 certificates=certificates_paginated, 
                                 stats=stats,
                                 current_filters={
                                     'type': certificate_type,
                                     'status': status_filter,
                                     'search': search_query,
                                     'date_from': date_from,
                                     'date_to': date_to
                                 },
                                 export_message="Excel export feature coming soon!")

    return render_template('clerk/certificates.html', 
                         certificates=certificates_paginated, 
                         stats=stats,
                         current_filters={
                             'type': certificate_type,
                             'status': status_filter,
                             'search': search_query,
                             'date_from': date_from,
                             'date_to': date_to
                         })

@clerk_bp.route('/officials')
@clerk_required
def officials():
    # Get all active officials
    officials_list = Official.query.filter_by(is_active=True).all()
    
    # Calculate statistics
    total_officials = len(officials_list)
    
    # Count positions
    positions_count = {}
    committees_count = {}
    
    for official in officials_list:
        positions_count[official.position] = positions_count.get(official.position, 0) + 1
        # For now, we'll use the position to determine committee (can be enhanced later)
        if 'Kagawad' in official.position:
            committee = getattr(official, 'committee', 'General')
            committees_count[committee] = committees_count.get(committee, 0) + 1
    
    # Calculate vacant positions (typical barangay structure has 7 kagawads + captain + secretary + treasurer)
    expected_positions = {
        'Barangay Captain': 1,
        'Barangay Kagawad': 7,
        'Secretary': 1,
        'Treasurer': 1,
        'SK Chairman': 1
    }
    
    current_positions = {}
    for official in officials_list:
        pos = official.position
        if 'Kagawad' in pos:
            pos = 'Barangay Kagawad'
        current_positions[pos] = current_positions.get(pos, 0) + 1
    
    vacant_positions = sum(max(0, expected_positions.get(pos, 0) - current_positions.get(pos, 0)) 
                          for pos in expected_positions)
    
    # Current term (you can make this dynamic)
    current_term = "2023-2026"
    next_election = "May 2026"
    
    stats = {
        'total_officials': total_officials,
        'current_term': current_term,
        'next_election': next_election,
        'vacant_positions': vacant_positions
    }
    
    # Group officials by committee for committee structure
    committees = {}
    for official in officials_list:
        if official.committee and official.committee != 'No Chairmanship':
            committee_name = official.committee.replace('Committee on ', '')
            if committee_name not in committees:
                committees[committee_name] = []
            committees[committee_name].append(official)
    
    return render_template('clerk/officials.html', 
                         officials=officials_list, 
                         stats=stats,
                         positions_count=positions_count,
                         committees=committees)

@clerk_bp.route('/announcements')
@clerk_required
def announcements():
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    
    # Build query
    query = Announcement.query
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Announcement.title.ilike(search_term),
                Announcement.content.ilike(search_term),
                Announcement.excerpt.ilike(search_term)
            )
        )
    
    # Apply category filter
    if category:
        query = query.filter(Announcement.category == category)
    
    # Apply status filter
    if status:
        query = query.filter(Announcement.status == status)
    
    # Apply priority filter
    if priority:
        query = query.filter(Announcement.priority == priority)
    
    # Order by pinned status first, then creation date (newest first)
    query = query.order_by(
        Announcement.is_pinned.desc(),
        Announcement.created_at.desc()
    )
    
    # Paginate results
    announcements = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    # Get statistics
    stats = get_announcement_stats()
    
    # Get current filters for template
    current_filters = {
        'search': search,
        'category': category,
        'status': status,
        'priority': priority
    }
    
    return render_template('clerk/announcements.html', 
                         announcements=announcements,
                         stats=stats,
                         current_filters=current_filters)

# Announcement API Endpoints
@clerk_bp.route('/api/announcements')
@clerk_required
def get_announcements_api():
    """Get announcements with filtering and pagination"""
    try:
        # Get parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        status = request.args.get('status', '')
        priority = request.args.get('priority', '')
        
        # Build query
        query = Announcement.query
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Announcement.title.ilike(search_term),
                    Announcement.content.ilike(search_term),
                    Announcement.excerpt.ilike(search_term)
                )
            )
        
        if category:
            query = query.filter(Announcement.category == category)
        
        if status:
            query = query.filter(Announcement.status == status)
            
        if priority:
            query = query.filter(Announcement.priority == priority)
        
        # Order and paginate
        query = query.order_by(Announcement.created_at.desc())
        announcements = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Format response
        result = {
            'success': True,
            'announcements': [{
                'id': ann.id,
                'title': ann.title,
                'excerpt': ann.excerpt,
                'category': ann.category,
                'formatted_category': ann.formatted_category,
                'status': ann.status,
                'formatted_status': ann.formatted_status,
                'priority': ann.priority,
                'is_featured': ann.is_featured,
                'is_pinned': ann.is_pinned,
                'publish_date': ann.publish_date.isoformat() if ann.publish_date else None,
                'created_at': ann.created_at.isoformat(),
                'author': ann.author.full_name if ann.author else 'Unknown'
            } for ann in announcements.items],
            'pagination': {
                'page': announcements.page,
                'pages': announcements.pages,
                'per_page': announcements.per_page,
                'total': announcements.total,
                'has_next': announcements.has_next,
                'has_prev': announcements.has_prev
            },
            'stats': get_announcement_stats()
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching announcements: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement/<int:announcement_id>', methods=['GET'])
@clerk_required
def get_announcement(announcement_id):
    """Get specific announcement details"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        result = {
            'success': True,
            'announcement': {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'excerpt': announcement.excerpt,
                'category': announcement.category,
                'formatted_category': announcement.formatted_category,
                'tags': announcement.get_tags_list(),
                'status': announcement.status,
                'formatted_status': announcement.formatted_status,
                'priority': announcement.priority,
                'is_featured': announcement.is_featured,
                'is_pinned': announcement.is_pinned,
                'publish_date': announcement.publish_date.isoformat() if announcement.publish_date else None,
                'expiry_date': announcement.expiry_date.isoformat() if announcement.expiry_date else None,
                'event_date': announcement.event_date.isoformat() if announcement.event_date else None,
                'event_time': announcement.event_time.isoformat() if announcement.event_time else None,
                'event_location': announcement.event_location,
                'event_organizer': announcement.event_organizer,
                'event_contact': announcement.event_contact,
                'send_sms': announcement.send_sms,
                'send_email': announcement.send_email,
                'post_on_website': announcement.post_on_website,
                'notify_residents': announcement.notify_residents,
                'attachment_name': announcement.attachment_name,
                'view_count': announcement.view_count,
                'created_at': announcement.created_at.isoformat(),
                'updated_at': announcement.updated_at.isoformat(),
                'author': announcement.author.full_name if announcement.author else 'Unknown'
            }
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching announcement: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement', methods=['POST'])
@clerk_required
def create_announcement():
    """Create new announcement"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('content'):
            return jsonify({
                'success': False,
                'message': 'Title and content are required'
            }), 400
        
        # Create slug from title
        import re
        from datetime import datetime
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', data['title'])
        slug = re.sub(r'\s+', '-', slug.strip()).lower()
        
        # Make slug unique by checking if it exists
        base_slug = slug
        counter = 1
        while Announcement.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create announcement
        announcement = Announcement(
            title=data['title'],
            content=data['content'],
            slug=slug,
            excerpt=data.get('excerpt', ''),
            category=data.get('category', 'general'),
            priority=data.get('priority', 'normal'),
            status=data.get('status', 'draft'),
            is_featured=data.get('is_featured', False),
            is_pinned=data.get('is_pinned', False),
            send_sms=data.get('send_sms', False),
            send_email=data.get('send_email', True),
            post_on_website=data.get('post_on_website', True),
            notify_residents=data.get('notify_residents', False),
            created_by=session['user']['id']
        )
        
        # Set tags if provided
        if data.get('tags'):
            if isinstance(data['tags'], list):
                announcement.set_tags_from_list(data['tags'])
            else:
                announcement.tags = data['tags']
        
        # Set dates if provided
        if data.get('publish_date'):
            try:
                announcement.publish_date = datetime.fromisoformat(data['publish_date'].replace('Z', '+00:00'))
            except:
                pass
                
        if data.get('expiry_date'):
            try:
                announcement.expiry_date = datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00'))
            except:
                pass
        
        # Set event details if provided
        if data.get('event_date'):
            try:
                announcement.event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
            except:
                pass
                
        if data.get('event_time'):
            announcement.event_time = data['event_time']
            
        announcement.event_location = data.get('event_location', '')
        announcement.event_organizer = data.get('event_organizer', '')
        announcement.event_contact = data.get('event_contact', '')
        
        # If publishing immediately, set published status
        if data.get('publish_now', False):
            announcement.status = 'published'
            announcement.is_published = True
            announcement.published_at = datetime.utcnow()
        
        db.session.add(announcement)
        db.session.commit()
        
        # Log activity
        log_announcement_action(
            ActivityTypes.ANNOUNCEMENT_CREATE,
            data['title'],
            announcement.id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Announcement created successfully',
            'announcement_id': announcement.id,
            'announcement_number': announcement.announcement_number
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating announcement: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement/<int:announcement_id>', methods=['PUT'])
@clerk_required
def update_announcement(announcement_id):
    """Update announcement"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            announcement.title = data['title']
            # Update slug
            import re
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', data['title'])
            announcement.slug = re.sub(r'\s+', '-', slug.strip()).lower()
            
        if 'content' in data:
            announcement.content = data['content']
            
        if 'excerpt' in data:
            announcement.excerpt = data['excerpt']
            
        if 'category' in data:
            announcement.category = data['category']
            
        if 'priority' in data:
            announcement.priority = data['priority']
            
        if 'status' in data:
            old_status = announcement.status
            announcement.status = data['status']
            
            # Handle status transitions
            if old_status != 'published' and data['status'] == 'published':
                announcement.is_published = True
                announcement.published_at = datetime.utcnow()
            elif data['status'] != 'published':
                announcement.is_published = False
                
        if 'is_featured' in data:
            announcement.is_featured = data['is_featured']
            
        if 'is_pinned' in data:
            announcement.is_pinned = data['is_pinned']
            
        if 'tags' in data:
            if isinstance(data['tags'], list):
                announcement.set_tags_from_list(data['tags'])
            else:
                announcement.tags = data['tags']
        
        # Update notification settings
        if 'send_sms' in data:
            announcement.send_sms = data['send_sms']
        if 'send_email' in data:
            announcement.send_email = data['send_email']
        if 'post_on_website' in data:
            announcement.post_on_website = data['post_on_website']
        if 'notify_residents' in data:
            announcement.notify_residents = data['notify_residents']
        
        # Update dates
        if 'publish_date' in data:
            try:
                announcement.publish_date = datetime.fromisoformat(data['publish_date'].replace('Z', '+00:00')) if data['publish_date'] else None
            except:
                pass
                
        if 'expiry_date' in data:
            try:
                announcement.expiry_date = datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00')) if data['expiry_date'] else None
            except:
                pass
        
        # Update event details
        if 'event_date' in data:
            try:
                announcement.event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00')) if data['event_date'] else None
            except:
                pass
                
        if 'event_time' in data:
            announcement.event_time = data['event_time']
            
        if 'event_location' in data:
            announcement.event_location = data['event_location']
            
        if 'event_organizer' in data:
            announcement.event_organizer = data['event_organizer']
            
        if 'event_contact' in data:
            announcement.event_contact = data['event_contact']
        
        # Update metadata
        announcement.updated_by = session['user']['id']
        announcement.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log activity
        log_announcement_action(
            ActivityTypes.ANNOUNCEMENT_UPDATE,
            announcement.title,
            announcement_id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Announcement updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating announcement: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement/<int:announcement_id>', methods=['DELETE'])
@clerk_required
def delete_announcement(announcement_id):
    """Delete announcement"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        announcement_title = announcement.title
        
        db.session.delete(announcement)
        db.session.commit()
        
        # Log activity
        log_announcement_action(
            ActivityTypes.ANNOUNCEMENT_DELETE,
            announcement_title,
            announcement_id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Announcement deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting announcement: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement/<int:announcement_id>/publish', methods=['POST'])
@clerk_required
def publish_announcement(announcement_id):
    """Publish announcement"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        
        announcement.status = 'published'
        announcement.is_published = True
        announcement.published_at = datetime.utcnow()
        announcement.approved_by = session['user']['id']
        announcement.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log activity
        log_announcement_action(
            ActivityTypes.ANNOUNCEMENT_PUBLISH,
            announcement.title,
            announcement_id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Announcement published successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error publishing announcement: {str(e)}'
        }), 500

@clerk_bp.route('/api/announcement/<int:announcement_id>/unpublish', methods=['POST'])
@clerk_required
def unpublish_announcement(announcement_id):
    """Unpublish announcement"""
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        
        announcement.status = 'draft'
        announcement.is_published = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Announcement unpublished successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error unpublishing announcement: {str(e)}'
        }), 500

@clerk_bp.route('/blotter')
@clerk_required
def blotter():
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    incident_type = request.args.get('type', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = BlotterRecord.query
    
    # Apply filters
    if search:
        query = query.filter(
            db.or_(
                BlotterRecord.case_number.ilike(f'%{search}%'),
                BlotterRecord.complainant_name.ilike(f'%{search}%'),
                BlotterRecord.respondent_name.ilike(f'%{search}%'),
                BlotterRecord.incident_place.ilike(f'%{search}%'),
                BlotterRecord.incident_description.ilike(f'%{search}%')
            )
        )
    
    if incident_type:
        query = query.filter(BlotterRecord.incident_type == incident_type)
    
    if status:
        query = query.filter(BlotterRecord.status == status)
    
    if priority:
        query = query.filter(BlotterRecord.priority == priority)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(BlotterRecord.incident_date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(BlotterRecord.incident_date <= date_to_obj)
        except ValueError:
            pass
    
    # Handle export
    export_format = request.args.get('export')
    if export_format in ['csv', 'excel']:
        blotters = query.order_by(BlotterRecord.created_at.desc()).all()
        return export_blotters(blotters, export_format)
    
    # Order and paginate
    blotters = query.order_by(BlotterRecord.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get statistics
    stats = get_blotter_stats()
    
    # Store current filters for template
    current_filters = {
        'search': search,
        'type': incident_type,
        'status': status,
        'priority': priority,
        'date_from': date_from,
        'date_to': date_to
    }
    
    return render_template('clerk/blotter.html', 
                         blotters=blotters, 
                         stats=stats,
                         current_filters=current_filters)

@clerk_bp.route('/payment-list')
@clerk_required
def payment_list():
    """Display payment list page showing completed certificates awaiting payment"""
    from models import Payment
    from sqlalchemy import func, extract
    from datetime import datetime, timedelta
    
    # Get filter parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    service_type = request.args.get('service_type', '')
    payment_status = request.args.get('payment_status', '')
    payment_method = request.args.get('payment_method', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Base query - show only paid certificate payments (exclude pending)
    query = Payment.query.filter(
        Payment.is_certificate_payment == True,
        Payment.payment_status == 'paid'
    ).join(Certificate, Payment.certificate_id == Certificate.id)
    
    # Apply filters
    if search:
        query = query.filter(
            Payment.payer_name.contains(search) |
            Payment.payment_number.contains(search) |
            Payment.reference_number.contains(search) |
            Payment.service_description.contains(search)
        )
    
    if service_type:
        query = query.filter(Payment.service_type == service_type)
    
    if payment_status:
        query = query.filter(Payment.payment_status == payment_status)
    
    if payment_method:
        query = query.filter(Payment.payment_method == payment_method)
    
    if date_from:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Payment.created_at >= date_from_obj)
    
    if date_to:
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        query = query.filter(Payment.created_at <= date_to_obj)
    
    # Get paginated results - prioritize completed certificates awaiting payment
    per_page = 10
    payments_paginated = query.order_by(
        # Show completed certificate payments first (those with certificate_id)
        # Use CASE statement for MySQL compatibility instead of nullslast()
        db.case(
            (Payment.certificate_id.isnot(None), 1),
            else_=0
        ).desc(),
        # Then by status - pending payments first
        Payment.payment_status.asc(),
        # Finally by creation date
        Payment.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Calculate statistics
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Total revenue (all paid payments)
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(payment_status='paid').scalar() or 0
    
    # This month revenue
    month_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.payment_status == 'paid',
        extract('month', Payment.payment_date) == current_month,
        extract('year', Payment.payment_date) == current_year
    ).scalar() or 0
    
    # Total transactions count (only paid certificate payments)
    total_transactions = Payment.query.filter(
        Payment.is_certificate_payment == True,
        Payment.payment_status == 'paid'
    ).count()
    
    stats = {
        'total_revenue': float(total_revenue),
        'month_revenue': float(month_revenue),
        'total_transactions': total_transactions
    }
    
    # Current filters for template
    current_filters = {
        'search': search,
        'service_type': service_type,
        'payment_status': payment_status,
        'payment_method': payment_method,
        'date_from': date_from,
        'date_to': date_to
    }
    
    return render_template('clerk/payment-list.html', 
                         payments=payments_paginated, 
                         stats=stats,
                         current_filters=current_filters)# Payment API Endpoints
@clerk_bp.route('/api/payment-list')
@clerk_required
def get_payment_list_api():
    """Get payments with filtering and pagination"""
    try:
        from models import Payment
        from sqlalchemy import func, extract
        from datetime import datetime
        
        # Get parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        service_type = request.args.get('service_type', '')
        payment_status = request.args.get('payment_status', '')
        payment_method = request.args.get('payment_method', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # Base query - show only paid certificate payments 
        query = Payment.query.filter(
            Payment.is_certificate_payment == True,
            Payment.payment_status == 'paid'
        )
        
        # Apply filters
        if search:
            query = query.filter(
                Payment.payer_name.contains(search) |
                Payment.payment_number.contains(search) |
                Payment.reference_number.contains(search) |
                Payment.service_description.contains(search)
            )
        
        if service_type:
            query = query.filter(Payment.service_type == service_type)
        
        if payment_status:
            query = query.filter(Payment.payment_status == payment_status)
        
        if payment_method:
            query = query.filter(Payment.payment_method == payment_method)
        
        if date_from:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Payment.created_at >= date_from_obj)
        
        if date_to:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Payment.created_at <= date_to_obj)
        
        # Get paginated results
        payments = query.order_by(Payment.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Convert to JSON format
        result = {
            'success': True,
            'payments': [{
                'id': payment.id,
                'payment_number': payment.payment_number,
                'reference_number': payment.reference_number,
                'payer_name': payment.payer_name,
                'payer_email': payment.payer_email,
                'service_type': payment.service_type,
                'service_description': payment.service_description,
                'amount': float(payment.amount),
                'total_amount': payment.total_amount,
                'formatted_amount': payment.formatted_amount,
                'payment_method': payment.payment_method,
                'payment_status': payment.payment_status,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                'due_date': payment.due_date.isoformat() if payment.due_date else None,
                'receipt_number': payment.receipt_number,
                'is_paid': payment.is_paid,
                'is_pending': payment.is_pending,
                'is_overdue': payment.is_overdue,
                'days_overdue': payment.days_overdue,
                'status_badge_class': payment.status_badge_class,
                'method_badge_class': payment.method_badge_class,
                'created_at': payment.created_at.isoformat(),
                'updated_at': payment.updated_at.isoformat()
            } for payment in payments.items],
            'pagination': {
                'page': payments.page,
                'pages': payments.pages,
                'per_page': payments.per_page,
                'total': payments.total,
                'has_next': payments.has_next,
                'has_prev': payments.has_prev
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching payments: {str(e)}'
        }), 500

@clerk_bp.route('/api/payment-list/<int:payment_id>')
@clerk_required
def get_payment_list_item_api(payment_id):
    """Get single payment details"""
    try:
        from models import Payment
        
        payment = Payment.query.get_or_404(payment_id)
        
        result = {
            'success': True,
            'payment': payment.to_dict()
        }
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/payment-list', methods=['POST'])
@clerk_required
def create_payment_list_item_api():
    """Create new payment"""
    try:
        from models import Payment, Resident
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['payer_name', 'service_type', 'amount', 'payment_method']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Find or create resident
        resident = None
        if data.get('resident_id'):
            resident = Resident.query.get(data['resident_id'])
        
        if not resident:
            # Use first resident as fallback
            resident = Resident.query.first()
            if not resident:
                return jsonify({
                    'success': False,
                    'message': 'No resident found. Please create a resident first.'
                }), 400
        
        # Handle certificate payment
        certificate = None
        if data.get('certificate_id'):
            certificate = Certificate.query.get(data['certificate_id'])
            if certificate:
                # Update service details based on certificate
                service_type = certificate.certificate_type
                service_description = f"{certificate.certificate_type.replace('_', ' ').title()} for {certificate.purpose}"
            else:
                service_type = data['service_type']
                service_description = data.get('service_description', '')
        else:
            service_type = data['service_type']
            service_description = data.get('service_description', '')

        # Create payment
        payment = Payment(
            resident_id=resident.id,
            certificate_id=certificate.id if certificate else None,
            payer_name=data['payer_name'],
            payer_email=data.get('payer_email', ''),
            payer_phone=data.get('payer_phone', ''),
            service_type=service_type,
            service_description=service_description,
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            payment_status=data.get('payment_status', 'pending'),
            reference_number=data.get('reference_number', ''),
            base_fee=float(data.get('base_fee', data['amount'])),
            additional_fees=float(data.get('additional_fees', 0)),
            discount_amount=float(data.get('discount_amount', 0)),
            tax_amount=float(data.get('tax_amount', 0)),
            payment_category=data.get('payment_category', 'service_fee'),
            priority=data.get('priority', 'normal'),
            notes=data.get('notes', ''),
            created_by=session.get('user_id', 1)
        )
        
        # Set due date if provided
        if data.get('due_date'):
            from datetime import datetime
            payment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        
        # If payment is marked as paid, set payment date
        if payment.payment_status == 'paid':
            payment.mark_as_paid(session.get('user_id', 1))
        
        # Update certificate payment status if this is a certificate payment
        if certificate:
            if payment.payment_status == 'paid':
                certificate.payment_status = 'paid'
                certificate.payment_date = datetime.utcnow()
            else:
                certificate.payment_status = 'pending_payment'
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': 'Payment created successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/payment-list/<int:payment_id>', methods=['PUT'])
@clerk_required
def update_payment_list_item_api(payment_id):
    """Update payment"""
    try:
        from models import Payment
        
        payment = Payment.query.get_or_404(payment_id)
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'payer_name', 'payer_email', 'payer_phone', 'service_type',
            'service_description', 'amount', 'payment_method', 'payment_status',
            'base_fee', 'additional_fees', 'discount_amount', 'tax_amount',
            'payment_category', 'priority', 'notes', 'reference_number'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field in ['amount', 'base_fee', 'additional_fees', 'discount_amount', 'tax_amount']:
                    setattr(payment, field, float(data[field]))
                else:
                    setattr(payment, field, data[field])
        
        # Handle due date
        if 'due_date' in data and data['due_date']:
            from datetime import datetime
            payment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        
        # Handle payment status changes
        if 'payment_status' in data:
            if data['payment_status'] == 'paid' and not payment.is_paid:
                payment.mark_as_paid(session.get('user_id', 1))
        
        payment.updated_by = session.get('user_id', 1)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': 'Payment updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/payments/<int:payment_id>', methods=['DELETE'])
@clerk_required
def delete_payment_api(payment_id):
    """Delete payment"""
    try:
        from models import Payment
        
        payment = Payment.query.get_or_404(payment_id)
        
        # Store payment info for response
        payment_info = {
            'payment_number': payment.payment_number,
            'payer_name': payment.payer_name,
            'amount': payment.formatted_amount
        }
        
        db.session.delete(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Payment {payment_info["payment_number"]} deleted successfully',
            'deleted_payment': payment_info
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/payment-list/<int:payment_id>/mark-paid', methods=['POST'])
@clerk_required
def mark_payment_list_paid_api(payment_id):
    """Mark certificate payment as paid and complete the certificate payment process"""
    try:
        from models import Payment
        
        payment = Payment.query.get_or_404(payment_id)
        
        # Ensure this is a certificate payment
        if not payment.is_certificate_payment:
            return jsonify({
                'success': False,
                'message': 'This is not a certificate payment'
            }), 400
        
        # Mark payment as paid
        payment.mark_as_paid(session.get('user_id', 1))
        payment.updated_by = session.get('user_id', 1)
        
        # Mark certificate payment as completed and move to payment list
        if payment.certificate:
            payment.certificate.mark_payment_completed_and_move_to_list(session.get('user_id', 1))
        
        db.session.commit()
        
        # Log activity
        log_payment_action(
            ActivityTypes.PAYMENT_RECEIVED,
            payment.payment_number,
            payment.amount,
            payment.payer_name,
            payment.id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': f'Certificate payment {payment.payment_number} completed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error processing payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/payments/<int:payment_id>/refund', methods=['POST'])
@clerk_required
def refund_payment_api(payment_id):
    """Process payment refund"""
    try:
        from models import Payment
        
        payment = Payment.query.get_or_404(payment_id)
        data = request.get_json()
        
        refund_amount = float(data.get('refund_amount', 0))
        refund_reason = data.get('refund_reason', '')
        
        if not refund_amount or refund_amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Invalid refund amount'
            }), 400
        
        if not refund_reason:
            return jsonify({
                'success': False,
                'message': 'Refund reason is required'
            }), 400
        
        # Process refund
        payment.process_refund(refund_amount, refund_reason, session.get('user_id', 1))
        payment.updated_by = session.get('user_id', 1)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': f'Refund of ₱{refund_amount:,.2f} processed successfully'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error processing refund: {str(e)}'
        }), 500

def get_payment_stats():
    """Helper function to get payment statistics"""
    from models import Payment
    from sqlalchemy import func, extract
    from datetime import datetime
    
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Basic counts
    total_payments = Payment.query.count()
    paid_count = Payment.query.filter_by(payment_status='paid').count()
    pending_count = Payment.query.filter_by(payment_status='pending').count()
    failed_count = Payment.query.filter_by(payment_status='failed').count()
    
    # Revenue calculations
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(payment_status='paid').scalar() or 0
    month_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.payment_status == 'paid',
        extract('month', Payment.payment_date) == current_month,
        extract('year', Payment.payment_date) == current_year
    ).scalar() or 0
    
    # Pending amounts
    pending_total = db.session.query(func.sum(Payment.amount)).filter_by(payment_status='pending').scalar() or 0
    
    # Overdue payments
    overdue_count = Payment.query.filter(
        Payment.payment_status == 'pending',
        Payment.due_date < current_date
    ).count()
    
    return {
        'total_payments': total_payments,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'failed_count': failed_count,
        'total_revenue': float(total_revenue),
        'month_revenue': float(month_revenue),
        'pending_total': float(pending_total),
        'overdue_count': overdue_count
    }

@clerk_bp.route('/settings')
@clerk_required
def settings():
    return render_template('clerk/settings.html')

@clerk_bp.route('/activity-log')
@clerk_required
def activity_log():
    # Get filter parameters
    activity_type = request.args.get('type', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    user_filter = request.args.get('user', '', type=int)
    page = request.args.get('page', 1, type=int)
    
    # Base query
    query = SystemActivity.query.join(User, SystemActivity.user_id == User.id, isouter=True)
    
    # Apply filters
    if activity_type:
        query = query.filter(SystemActivity.activity_type == activity_type)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(SystemActivity.created_at >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            # Add one day to include the full day
            to_date = to_date.replace(hour=23, minute=59, second=59)
            query = query.filter(SystemActivity.created_at <= to_date)
        except ValueError:
            pass
    
    if user_filter:
        query = query.filter(SystemActivity.user_id == user_filter)
    
    # Order by newest first and paginate
    activities = query.order_by(SystemActivity.created_at.desc()).paginate(
        page=page, per_page=25, error_out=False
    )
    
    # Get unique activity types for filter dropdown
    activity_types = db.session.query(SystemActivity.activity_type).distinct().all()
    activity_types = [a[0] for a in activity_types if a[0]]
    
    # Get users who have performed activities
    active_users = db.session.query(User).join(SystemActivity).distinct().all()
    
    return render_template('clerk/activity-log.html', 
                         activities=activities,
                         activity_types=activity_types,
                         active_users=active_users,
                         current_filters={
                             'type': activity_type,
                             'date_from': date_from,
                             'date_to': date_to,
                             'user': user_filter
                         })

# API endpoints for AJAX requests
@clerk_bp.route('/api/approve-resident/<int:resident_id>', methods=['POST'])
@clerk_required
def approve_resident(resident_id):
    resident = Resident.query.get_or_404(resident_id)
    resident.status = 'approved'
    db.session.commit()
    
    # Log system activity using the utility function
    log_resident_action(
        ActivityTypes.RESIDENT_APPROVAL,
        resident.full_name,
        resident_id,
        user_id=session.get('user', {}).get('id')
    )
    
    return jsonify({'status': 'success', 'message': 'Resident approved successfully'})

# API endpoint for getting resident details
@clerk_bp.route('/api/resident-details/<int:resident_id>', methods=['GET'])
@clerk_required
def get_resident_details(resident_id):
    try:
        resident = Resident.query.get_or_404(resident_id)
        
        # Get purok/sitio name if exists
        purok_name = resident.sitio.name if resident.sitio else None
        
        resident_data = {
            'id': resident.id,
            'full_name': resident.full_name,
            'first_name': resident.first_name,
            'middle_name': resident.middle_name,
            'last_name': resident.last_name,
            'suffix': resident.suffix,
            'email': resident.email,
            'phone': resident.phone,
            'full_address': resident.full_address,  # Use the property defined in the model
            'house_number': resident.house_number,
            'purok': purok_name,
            'birth_date': resident.birth_date.strftime('%Y-%m-%d') if resident.birth_date else None,
            'birth_place': resident.birth_place,
            'gender': resident.gender,
            'civil_status': resident.civil_status,
            'occupation': resident.occupation,
            'profile_picture': resident.profile_picture,
            'valid_id_document': resident.valid_id_document,
            'proof_of_residency': resident.proof_of_residency,
            'status': resident.status,
            'is_voter': resident.is_voter,
            'created_at': resident.created_at.isoformat() if resident.created_at else None,
            'updated_at': resident.updated_at.isoformat() if resident.updated_at else None
        }
        
        return jsonify({'status': 'success', 'resident': resident_data})
        
    except Exception as e:
        print(f"Error getting resident details: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to get resident details'})

# Enhanced API endpoint for rejecting residents with email notification
@clerk_bp.route('/api/reject-resident/<int:resident_id>', methods=['POST'])
@clerk_required
def reject_resident_with_reason(resident_id):
    try:
        data = request.get_json()
        rejection_reason = data.get('rejection_reason', '').strip()
        
        if not rejection_reason:
            return jsonify({'status': 'error', 'message': 'Rejection reason is required'})
        
        resident = Resident.query.get_or_404(resident_id)
        
        # Store the rejection reason (you might want to add a rejection_reason field to the model)
        resident.status = 'rejected'
        
        # Log the rejection reason in system activity
        log_resident_action(
            ActivityTypes.RESIDENT_REJECTION,
            f"{resident.full_name} - Reason: {rejection_reason}",
            resident_id,
            user_id=session.get('user', {}).get('id')
        )
        
        db.session.commit()
        
        # Send email notification if resident has an email
        if resident.email:
            try:
                send_rejection_email(resident, rejection_reason)
            except Exception as email_error:
                print(f"Warning: Failed to send rejection email to {resident.email}: {email_error}")
                # Don't fail the rejection if email fails
        
        return jsonify({'status': 'success', 'message': 'Resident rejected and notified'})
        
    except Exception as e:
        print(f"Error rejecting resident: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to reject resident'})

# Email sending function
def send_rejection_email(resident, rejection_reason):
    """Send rejection notification email to resident"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from flask import current_app
        
        # Get email configuration from app config
        mail_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
        mail_port = current_app.config.get('MAIL_PORT', 587)
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')
        
        if not mail_username or not mail_password:
            print("Warning: Email credentials not configured. Set MAIL_USERNAME and MAIL_PASSWORD environment variables.")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = mail_username
        msg['To'] = resident.email
        msg['Subject'] = "Barangay Resident Application - Status Update"
        
        # Create email body
        body = f"""
Dear {resident.first_name} {resident.last_name},

We hope this message finds you well.

We have reviewed your application for barangay residency registration, and unfortunately, we must inform you that your application has been declined at this time.

Reason for Rejection:
{rejection_reason}

What you can do next:
- Please review the reason provided above
- Address any issues mentioned in the rejection reason
- You may resubmit your application once the concerns have been resolved
- If you have questions, please visit our office during business hours

We appreciate your understanding and encourage you to address the mentioned concerns so you can reapply.

Best regards,
Barangay iSerBisyo Team

---
This is an automated message. Please do not reply to this email.
For inquiries, please visit the barangay office or contact us through official channels.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        text = msg.as_string()
        server.sendmail(mail_username, resident.email, text)
        server.quit()
        
        print(f"Rejection email sent successfully to {resident.email}")
        
    except Exception as e:
        print(f"Error sending rejection email: {e}")
        raise e

# API endpoints for officials management
@clerk_bp.route('/api/add-official', methods=['POST'])
@clerk_required
def add_official():
    try:
        # Handle both JSON and FormData
        if request.content_type and 'multipart/form-data' in request.content_type:
            # FormData from file upload
            name = request.form.get('name')
            position = request.form.get('position')
            committee = request.form.get('committee')
            email = request.form.get('email')
            phone = request.form.get('phone')
            term_start = request.form.get('term_start')
            
            # Handle profile picture upload
            profile_picture_filename = None
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                profile_picture_filename = save_profile_picture(file)
        else:
            # JSON data (backward compatibility)
            data = request.get_json()
            name = data.get('name')
            position = data.get('position')
            committee = data.get('committee')
            email = data.get('email')
            phone = data.get('phone')
            term_start = data.get('term_start')
            profile_picture_filename = None
        
        official = Official(
            name=name,
            position=position,
            committee=committee,
            email=email,
            phone=phone,
            profile_picture=profile_picture_filename,
            term_start=datetime.strptime(term_start, '%Y-%m-%d').date() if term_start else None
        )
        
        # Calculate term end (typically 3 years)
        if official.term_start:
            official.term_end = official.term_start.replace(year=official.term_start.year + 3)
        
        db.session.add(official)
        db.session.commit()
        
        # Log activity
        log_official_action(
            ActivityTypes.OFFICIAL_CREATE,
            name,
            official.id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({'status': 'success', 'message': 'Official added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@clerk_bp.route('/api/update-official/<int:official_id>', methods=['POST'])
@clerk_required
def update_official(official_id):
    try:
        official = Official.query.get_or_404(official_id)
        
        # Handle both JSON and FormData
        if request.content_type and 'multipart/form-data' in request.content_type:
            # FormData from file upload
            name = request.form.get('name')
            position = request.form.get('position')
            committee = request.form.get('committee')
            email = request.form.get('email')
            phone = request.form.get('phone')
            term_start = request.form.get('term_start')
            
            # Handle profile picture upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                new_profile_picture = save_profile_picture(file)
                if new_profile_picture:
                    # Delete old profile picture if it exists
                    if official.profile_picture:
                        old_file_path = os.path.join('static', 'uploads', 'profiles', official.profile_picture)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    official.profile_picture = new_profile_picture
        else:
            # JSON data (backward compatibility)
            data = request.get_json()
            name = data.get('name', official.name)
            position = data.get('position', official.position)
            committee = data.get('committee', official.committee)
            email = data.get('email', official.email)
            phone = data.get('phone', official.phone)
            term_start = data.get('term_start')
        
        official.name = name if name is not None else official.name
        official.position = position if position is not None else official.position
        official.committee = committee if committee is not None else official.committee
        official.email = email if email is not None else official.email
        official.phone = phone if phone is not None else official.phone
        
        if term_start:
            official.term_start = datetime.strptime(term_start, '%Y-%m-%d').date()
            official.term_end = official.term_start.replace(year=official.term_start.year + 3)
        
        official.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log activity
        log_official_action(
            ActivityTypes.OFFICIAL_UPDATE,
            official.name,
            official_id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({'status': 'success', 'message': 'Official updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@clerk_bp.route('/api/delete-official/<int:official_id>', methods=['POST'])
@clerk_required
def delete_official(official_id):
    try:
        official = Official.query.get_or_404(official_id)
        official_name = official.name
        
        db.session.delete(official)
        db.session.commit()
        
        # Log activity
        log_official_action(
            ActivityTypes.OFFICIAL_DELETE,
            official_name,
            official_id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({'status': 'success', 'message': 'Official deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@clerk_bp.route('/api/get-official/<int:official_id>')
@clerk_required
def get_official(official_id):
    official = Official.query.get_or_404(official_id)
    return jsonify({
        'id': official.id,
        'name': official.name,
        'position': official.position,
        'committee': official.committee,
        'email': official.email,
        'phone': official.phone,
        'profile_picture': official.profile_picture,
        'term_start': official.term_start.isoformat() if official.term_start else None,
        'term_end': official.term_end.isoformat() if official.term_end else None
    })

# Resident API Endpoints
@clerk_bp.route('/api/get-resident/<int:resident_id>')
@clerk_required
def get_resident(resident_id):
    """Get resident details for editing/viewing"""
    resident = Resident.query.get_or_404(resident_id)
    return jsonify({
        'id': resident.id,
        'first_name': resident.first_name,
        'middle_name': resident.middle_name,
        'last_name': resident.last_name,
        'suffix': resident.suffix,
        'email': resident.email,
        'phone': resident.phone,
        'house_number': resident.house_number,
        'street': '',  # Not in model, kept for compatibility
        'purok': resident.sitio.name if resident.sitio else '',
        'sitio_id': resident.sitio_id,
        'birth_date': resident.birth_date.isoformat() if resident.birth_date else None,
        'birth_place': resident.birth_place,
        'gender': resident.gender,
        'civil_status': resident.civil_status,
        'occupation': resident.occupation,
        'status': resident.status,
        'is_voter': resident.is_voter,
        'full_name': resident.full_name,
        'full_address': resident.full_address
    })

@clerk_bp.route('/api/add-resident', methods=['POST'])
@clerk_required
def add_resident():
    """Add new resident"""
    try:
        data = request.get_json()
        
        # Create new resident
        resident = Resident(
            first_name=data.get('first_name', '').strip(),
            middle_name=data.get('middle_name', '').strip() or None,
            last_name=data.get('last_name', '').strip(),
            suffix=data.get('suffix', '').strip() or None,
            email=data.get('email', '').strip() or None,
            phone=data.get('phone', '').strip() or None,
            house_number=data.get('house_number', '').strip() or None,
            sitio_id=data.get('sitio_id') or None,
            birth_place=data.get('birth_place', '').strip() or None,
            gender=data.get('gender', '').strip() or None,
            civil_status=data.get('civil_status', '').strip() or None,
            occupation=data.get('occupation', '').strip() or None,
            status=data.get('status', 'approved'),  # Default to approved for admin-created residents
            is_voter=data.get('is_voter', False)
        )
        
        # Handle birth_date
        if data.get('birth_date'):
            from datetime import datetime
            try:
                resident.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        db.session.add(resident)
        db.session.commit()
        
        # Log activity
        log_resident_action(
            ActivityTypes.RESIDENT_REGISTRATION,
            f"{resident.first_name} {resident.last_name}",
            resident.id,
            user_id=session.get('user', {}).get('id')
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Resident added successfully',
            'resident_id': resident.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to add resident: {str(e)}'
        }), 400

@clerk_bp.route('/api/update-resident/<int:resident_id>', methods=['POST'])
@clerk_required
def update_resident(resident_id):
    """Update existing resident"""
    try:
        resident = Resident.query.get_or_404(resident_id)
        data = request.get_json()
        
        # Update resident fields
        resident.first_name = data.get('first_name', resident.first_name).strip()
        resident.middle_name = data.get('middle_name', '').strip() or None
        resident.last_name = data.get('last_name', resident.last_name).strip()
        resident.suffix = data.get('suffix', '').strip() or None
        resident.email = data.get('email', '').strip() or None
        resident.phone = data.get('phone', '').strip() or None
        resident.house_number = data.get('house_number', '').strip() or None
        resident.sitio_id = data.get('sitio_id') or None
        resident.birth_place = data.get('birth_place', '').strip() or None
        resident.gender = data.get('gender', resident.gender)
        resident.civil_status = data.get('civil_status', resident.civil_status)
        resident.occupation = data.get('occupation', '').strip() or None
        resident.is_voter = data.get('is_voter', resident.is_voter)
        
        # Handle birth_date
        if data.get('birth_date'):
            from datetime import datetime
            try:
                resident.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        resident.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Resident updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update resident: {str(e)}'
        }), 400

@clerk_bp.route('/api/delete-resident/<int:resident_id>', methods=['POST'])
@clerk_required
def delete_resident(resident_id):
    """Delete resident (soft delete by changing status)"""
    try:
        resident = Resident.query.get_or_404(resident_id)
        
        # Soft delete by changing status to inactive
        resident.status = 'inactive'
        resident.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Resident removed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to remove resident: {str(e)}'
        }), 400

@clerk_bp.route('/api/archived-residents')
@clerk_required
def get_archived_residents():
    """Get all archived (inactive) residents"""
    try:
        from datetime import date
        
        archived_residents = Resident.query.filter_by(status='inactive').order_by(Resident.updated_at.desc()).all()
        
        residents_data = []
        for resident in archived_residents:
            # Calculate age from birth_date
            age = 'N/A'
            if resident.birth_date:
                today = date.today()
                age = today.year - resident.birth_date.year - ((today.month, today.day) < (resident.birth_date.month, resident.birth_date.day))
            
            # Get purok name if sitio relationship exists
            purok_name = 'N/A'
            if resident.sitio:
                purok_name = resident.sitio.name
            
            residents_data.append({
                'id': resident.id,
                'fullname': resident.full_name,
                'age': age,
                'gender': resident.gender or 'N/A',
                'purok': purok_name,
                'archived_date': resident.updated_at.strftime('%Y-%m-%d') if resident.updated_at else 'N/A'
            })
        
        return jsonify({
            'status': 'success',
            'residents': residents_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to load archived residents: {str(e)}'
        }), 500

@clerk_bp.route('/api/restore-resident/<int:resident_id>', methods=['POST'])
@clerk_required
def restore_resident(resident_id):
    """Restore archived resident (set status back to approved)"""
    try:
        resident = Resident.query.get_or_404(resident_id)
        
        # Restore by changing status back to approved
        resident.status = 'approved'
        resident.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Resident restored successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to restore resident: {str(e)}'
        }), 400

# Residents API Endpoint
@clerk_bp.route('/api/residents')
@clerk_required
def api_get_residents():
    """Get all approved residents for dropdown selection"""
    try:
        residents = Resident.query.filter_by(status='approved').order_by(Resident.first_name, Resident.last_name).all()
        residents_data = []
        for resident in residents:
            residents_data.append({
                'id': resident.id,
                'first_name': resident.first_name,
                'last_name': resident.last_name,
                'full_name': resident.full_name
            })
        
        return jsonify({
            'success': True,
            'residents': residents_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to load residents: {str(e)}'
        }), 500

# Certificate API Endpoints
@clerk_bp.route('/api/get-certificate/<int:certificate_id>')
@clerk_required
def get_certificate(certificate_id):
    """Get certificate details for editing/viewing"""
    certificate = Certificate.query.options(db.joinedload(Certificate.resident)).get_or_404(certificate_id)
    return jsonify({
        'id': certificate.id,
        'resident_id': certificate.resident_id,
        'resident_name': certificate.resident.full_name,
        'certificate_type': certificate.certificate_type,
        'purpose': certificate.purpose,
        'status': certificate.status,
        'fee': float(certificate.fee) if certificate.fee else 0.0,
        'payment_status': certificate.payment_status,
        'certificate_number': certificate.certificate_number,
        'notes': certificate.notes,
        'request_date': certificate.request_date.isoformat() if certificate.request_date else None,
        'processed_date': certificate.processed_date.isoformat() if certificate.processed_date else None,
        'claimed_date': certificate.claimed_date.isoformat() if certificate.claimed_date else None,
        'payment_date': certificate.payment_date.isoformat() if certificate.payment_date else None
    })

@clerk_bp.route('/api/add-certificate', methods=['POST'])
@clerk_required
def add_certificate():
    """Add new certificate request"""
    try:
        data = request.get_json()
        
        # Validate resident exists
        resident = Resident.query.get(data.get('resident_id'))
        if not resident:
            return jsonify({
                'status': 'error',
                'message': 'Resident not found'
            }), 400
        
        # Create new certificate
        certificate = Certificate(
            resident_id=data.get('resident_id'),
            certificate_type=data.get('certificate_type', '').strip(),
            purpose=data.get('purpose', '').strip() or None,
            status=data.get('status', 'pending'),
            fee=Decimal(str(data.get('fee', 0))),
            payment_status=data.get('payment_status', 'unpaid'),
            notes=data.get('notes', '').strip() or None
        )
        
        # Generate certificate number if approved
        if certificate.status in ['approved', 'ready', 'completed']:
            certificate.certificate_number = f"CERT-{datetime.utcnow().year}-{Certificate.query.count() + 1:04d}"
            certificate.processed_date = datetime.utcnow()
            certificate.processed_by = session.get('user', {}).get('id')
        
        # Set payment date if paid
        if certificate.payment_status == 'paid':
            certificate.payment_date = datetime.utcnow()
        
        db.session.add(certificate)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Certificate request added successfully',
            'certificate_id': certificate.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to add certificate: {str(e)}'
        }), 400

@clerk_bp.route('/api/update-certificate/<int:certificate_id>', methods=['POST'])
@clerk_required
def update_certificate(certificate_id):
    """Update existing certificate"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        data = request.get_json()
        
        old_status = certificate.status
        old_payment_status = certificate.payment_status
        
        # Update certificate fields
        certificate.certificate_type = data.get('certificate_type', certificate.certificate_type)
        certificate.purpose = data.get('purpose', '').strip() or None
        certificate.status = data.get('status', certificate.status)
        certificate.fee = Decimal(str(data.get('fee', certificate.fee)))
        certificate.payment_status = data.get('payment_status', certificate.payment_status)
        certificate.notes = data.get('notes', '').strip() or None
        
        # Generate certificate number if status changed to approved/ready/completed
        if old_status in ['pending', 'processing'] and certificate.status in ['approved', 'ready', 'completed']:
            if not certificate.certificate_number:
                certificate.certificate_number = f"CERT-{datetime.utcnow().year}-{Certificate.query.count():04d}"
            certificate.processed_date = datetime.utcnow()
            certificate.processed_by = session.get('user', {}).get('id')
        
        # Set payment date if payment status changed to paid
        if old_payment_status == 'unpaid' and certificate.payment_status == 'paid':
            certificate.payment_date = datetime.utcnow()
        
        # Set claimed date if status changed to completed
        if old_status != 'completed' and certificate.status == 'completed':
            certificate.claimed_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Certificate updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update certificate: {str(e)}'
        }), 400

@clerk_bp.route('/api/update-certificate-status/<int:certificate_id>', methods=['POST'])
@clerk_required
def update_certificate_status(certificate_id):
    """Update certificate status only"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        data = request.get_json()
        
        old_status = certificate.status
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'status': 'error',
                'message': 'Status is required'
            }), 400
        
        certificate.status = new_status
        
        # Generate certificate number if approved
        if old_status in ['pending', 'processing'] and new_status in ['approved', 'ready', 'completed']:
            if not certificate.certificate_number:
                certificate.certificate_number = f"CERT-{datetime.utcnow().year}-{Certificate.query.count():04d}"
            certificate.processed_date = datetime.utcnow()
            certificate.processed_by = session.get('user', {}).get('id')
        
        # Set claimed date if completed
        if old_status != 'completed' and new_status == 'completed':
            certificate.claimed_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Certificate status updated to {new_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update status: {str(e)}'
        }), 400

@clerk_bp.route('/api/update-payment-status/<int:certificate_id>', methods=['POST'])
@clerk_required
def update_payment_status(certificate_id):
    """Update certificate payment status"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        data = request.get_json()
        
        old_payment_status = certificate.payment_status
        new_payment_status = data.get('payment_status')
        
        if not new_payment_status:
            return jsonify({
                'status': 'error',
                'message': 'Payment status is required'
            }), 400
        
        certificate.payment_status = new_payment_status
        
        # Set payment date if paid
        if old_payment_status == 'unpaid' and new_payment_status == 'paid':
            certificate.payment_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Payment status updated to {new_payment_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to update payment status: {str(e)}'
        }), 400

@clerk_bp.route('/api/delete-certificate/<int:certificate_id>', methods=['POST'])
@clerk_required
def delete_certificate(certificate_id):
    """Delete certificate request"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Only allow deletion of pending or rejected certificates
        if certificate.status not in ['pending', 'rejected']:
            return jsonify({
                'status': 'error',
                'message': 'Only pending or rejected certificates can be deleted'
            }), 400
        
        db.session.delete(certificate)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Certificate request deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete certificate: {str(e)}'
        }), 400

@clerk_bp.route('/api/get-residents-for-certificate')
@clerk_required
def get_residents_for_certificate():
    """Get list of residents for certificate creation"""
    search = request.args.get('search', '')
    
    query = Resident.query.filter_by(status='approved')
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Resident.first_name.ilike(search_term),
                Resident.last_name.ilike(search_term)
            )
        )
    
    residents = query.limit(20).all()
    
    return jsonify({
        'success': True,
        'residents': [{
            'id': resident.id,
            'first_name': resident.first_name,
            'last_name': resident.last_name,
            'full_name': resident.full_name,
            'address': resident.full_address
        } for resident in residents]
    })

# Blotter API Endpoints
@clerk_bp.route('/api/blotter', methods=['GET'])
@clerk_required
def get_blotters():
    """Get paginated blotter records with filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        query = BlotterRecord.query
        
        # Apply filters if provided
        search = request.args.get('search')
        if search:
            query = query.filter(
                db.or_(
                    BlotterRecord.case_number.ilike(f'%{search}%'),
                    BlotterRecord.complainant_name.ilike(f'%{search}%'),
                    BlotterRecord.respondent_name.ilike(f'%{search}%')
                )
            )
        
        # Order by creation date (newest first)
        query = query.order_by(BlotterRecord.created_at.desc())
        
        # Paginate
        blotters = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = {
            'success': True,
            'blotters': [{
                'id': blotter.id,
                'case_number': blotter.case_number,
                'blotter_number': blotter.blotter_number,
                'complainant_name': blotter.complainant_name,
                'respondent_name': blotter.respondent_name,
                'incident_date': blotter.incident_date.isoformat() if blotter.incident_date else None,
                'incident_type': blotter.incident_type,
                'formatted_incident_type': blotter.formatted_incident_type,
                'incident_place': blotter.incident_place,
                'incident_description': blotter.incident_description,
                'status': blotter.status,
                'formatted_status': blotter.formatted_status,
                'priority': blotter.priority,
                'reported_by': blotter.reported_by,
                'reporter_type': blotter.reporter_type,
                'created_at': blotter.created_at.isoformat()
            } for blotter in blotters.items],
            'pagination': {
                'page': blotters.page,
                'pages': blotters.pages,
                'per_page': blotters.per_page,
                'total': blotters.total,
                'has_next': blotters.has_next,
                'has_prev': blotters.has_prev
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching blotters: {str(e)}'
        }), 500

@clerk_bp.route('/api/blotter/<int:blotter_id>', methods=['GET'])
@clerk_required
def get_blotter(blotter_id):
    """Get specific blotter record details"""
    try:
        blotter = BlotterRecord.query.get_or_404(blotter_id)
        
        result = {
            'success': True,
            'blotter': {
                'id': blotter.id,
                'case_number': blotter.case_number,
                'blotter_number': blotter.blotter_number,
                'complainant_name': blotter.complainant_name,
                'complainant_address': blotter.complainant_address,
                'complainant_contact': blotter.complainant_contact,
                'respondent_name': blotter.respondent_name,
                'respondent_address': blotter.respondent_address,
                'respondent_contact': blotter.respondent_contact,
                'incident_date': blotter.incident_date.isoformat() if blotter.incident_date else None,
                'incident_time': blotter.incident_time.isoformat() if blotter.incident_time else None,
                'incident_place': blotter.incident_place,
                'incident_type': blotter.incident_type,
                'formatted_incident_type': blotter.formatted_incident_type,
                'incident_description': blotter.incident_description,
                'status': blotter.status,
                'formatted_status': blotter.formatted_status,
                'priority': blotter.priority,
                'reported_by': blotter.reported_by,
                'reporter_type': blotter.reporter_type,
                'witnesses': blotter.witnesses,
                'evidence': blotter.evidence,
                'remarks': blotter.remarks,
                'resolution_date': blotter.resolution_date.isoformat() if blotter.resolution_date else None,
                'resolution_details': blotter.resolution_details,
                'created_at': blotter.created_at.isoformat(),
                'updated_at': blotter.updated_at.isoformat()
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching blotter: {str(e)}'
        }), 500

@clerk_bp.route('/api/blotter', methods=['POST'])
@clerk_required
def create_blotter():
    """Create new blotter record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['complainant_name', 'respondent_name', 'incident_date', 'incident_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field.replace("_", " ").title()} is required'
                }), 400
        
        # Generate case number
        year = datetime.utcnow().year
        last_blotter = BlotterRecord.query.filter(
            db.extract('year', BlotterRecord.created_at) == year
        ).order_by(BlotterRecord.id.desc()).first()
        
        next_number = (last_blotter.id + 1) if last_blotter else 1
        case_number = f"BLOT-{year}-{str(next_number).zfill(3)}"
        
        # Parse incident date and time
        incident_date = datetime.strptime(data['incident_date'], '%Y-%m-%d')
        incident_time = None
        if data.get('incident_time'):
            incident_time = datetime.strptime(data['incident_time'], '%H:%M').time()
        
        # Create blotter record
        blotter = BlotterRecord(
            case_number=case_number,
            complainant_name=data['complainant_name'],
            complainant_address=data.get('complainant_address'),
            complainant_contact=data.get('complainant_contact'),
            respondent_name=data['respondent_name'],
            respondent_address=data.get('respondent_address'),
            respondent_contact=data.get('respondent_contact'),
            incident_date=incident_date,
            incident_time=incident_time,
            incident_place=data.get('incident_place'),
            incident_type=data['incident_type'],
            incident_description=data.get('incident_description'),
            priority=data.get('priority', 'medium'),
            reported_by=data.get('reported_by'),
            reporter_type=data.get('reporter_type'),
            witnesses=data.get('witnesses'),
            evidence=data.get('evidence'),
            remarks=data.get('remarks'),
            recorded_by=session.get('user', {}).get('id')
        )
        
        db.session.add(blotter)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Blotter record created successfully',
            'blotter_id': blotter.id,
            'case_number': blotter.case_number
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating blotter: {str(e)}'
        }), 500

@clerk_bp.route('/api/blotter/<int:blotter_id>', methods=['PUT'])
@clerk_required
def update_blotter(blotter_id):
    """Update blotter record"""
    try:
        blotter = BlotterRecord.query.get_or_404(blotter_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'complainant_name' in data:
            blotter.complainant_name = data['complainant_name']
        if 'respondent_name' in data:
            blotter.respondent_name = data['respondent_name']
        if 'incident_date' in data:
            blotter.incident_date = datetime.strptime(data['incident_date'], '%Y-%m-%d')
        if 'incident_time' in data and data['incident_time']:
            blotter.incident_time = datetime.strptime(data['incident_time'], '%H:%M').time()
        if 'incident_place' in data:
            blotter.incident_place = data['incident_place']
        if 'incident_type' in data:
            blotter.incident_type = data['incident_type']
        if 'incident_description' in data:
            blotter.incident_description = data['incident_description']
        if 'status' in data:
            blotter.status = data['status']
            # If resolved, set resolution date
            if data['status'] in ['resolved', 'closed'] and not blotter.resolution_date:
                blotter.resolution_date = datetime.utcnow()
                blotter.resolved_by = session.get('user', {}).get('id')
        if 'priority' in data:
            blotter.priority = data['priority']
        if 'reported_by' in data:
            blotter.reported_by = data['reported_by']
        if 'reporter_type' in data:
            blotter.reporter_type = data['reporter_type']
        if 'resolution_details' in data:
            blotter.resolution_details = data['resolution_details']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Blotter record updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating blotter: {str(e)}'
        }), 500

@clerk_bp.route('/api/blotter/<int:blotter_id>', methods=['DELETE'])
@clerk_required
def delete_blotter(blotter_id):
    """Delete blotter record"""
    try:
        blotter = BlotterRecord.query.get_or_404(blotter_id)
        
        db.session.delete(blotter)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Blotter record deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting blotter: {str(e)}'
        }), 500

# Print Blotter Routes
@clerk_bp.route('/blotter/<int:blotter_id>/print')
@clerk_required
def print_single_blotter(blotter_id):
    """Print individual blotter record"""
    try:
        blotter = BlotterRecord.query.get_or_404(blotter_id)
        barangay_info = BarangayInfo.query.first()
        current_datetime = datetime.now().strftime('%B %d, %Y %I:%M %p')
        
        return render_template('clerk/print-blotter-single.html',
                             blotter=blotter,
                             barangay_info=barangay_info,
                             current_datetime=current_datetime)
    except Exception as e:
        flash(f'Error loading blotter for printing: {str(e)}', 'error')
        return redirect(url_for('clerk.blotter'))

@clerk_bp.route('/blotter/print')
@clerk_required
def print_blotter_report():
    """Print blotter report with filters"""
    try:
        # Get filter parameters
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        status = request.args.get('status')
        incident_type = request.args.get('type')
        priority = request.args.get('priority')
        
        # Base query
        query = BlotterRecord.query
        
        # Apply filters
        if date_from:
            query = query.filter(BlotterRecord.incident_date >= date_from)
        if date_to:
            query = query.filter(BlotterRecord.incident_date <= date_to)
        if status:
            query = query.filter(BlotterRecord.status == status)
        if incident_type:
            query = query.filter(BlotterRecord.incident_type == incident_type)
        if priority:
            query = query.filter(BlotterRecord.priority == priority)
        
        # Get all matching records
        blotters = query.order_by(BlotterRecord.incident_date.desc()).all()
        barangay_info = BarangayInfo.query.first()
        current_datetime = datetime.now().strftime('%B %d, %Y %I:%M %p')
        
        # Prepare filter info for display
        filter_info = {
            'date_from': date_from,
            'date_to': date_to,
            'status': status,
            'type': incident_type,
            'priority': priority
        }
        
        return render_template('clerk/print-blotter-report.html',
                             blotters=blotters,
                             barangay_info=barangay_info,
                             filter_info=filter_info,
                             current_datetime=current_datetime)
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('clerk.blotter'))

# Helper Functions
def get_blotter_stats():
    """Get blotter statistics for dashboard"""
    try:
        total_records = BlotterRecord.query.count()
        
        # This month's records
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month = BlotterRecord.query.filter(
            BlotterRecord.created_at >= current_month
        ).count()
        
        # Active cases (not resolved/closed)
        active_cases = BlotterRecord.query.filter(
            BlotterRecord.status.in_(['active', 'under_investigation', 'mediation_scheduled', 'referred_to_police'])
        ).count()
        
        # Resolved cases
        resolved_cases = BlotterRecord.query.filter(
            BlotterRecord.status.in_(['resolved', 'closed'])
        ).count()
        
        return {
            'total_records': total_records,
            'this_month': this_month,
            'active_cases': active_cases,
            'resolved_cases': resolved_cases
        }
        
    except Exception as e:
        print(f"Error getting blotter stats: {e}")
        return {
            'total_records': 0,
            'this_month': 0,
            'active_cases': 0,
            'resolved_cases': 0
        }

def get_announcement_stats():
    """Get announcement statistics for dashboard"""
    try:
        total_announcements = Announcement.query.count()
        
        # Published announcements
        published = Announcement.query.filter_by(status='published').count()
        
        # Draft announcements
        draft = Announcement.query.filter_by(status='draft').count()
        
        # Scheduled announcements
        scheduled = Announcement.query.filter_by(status='scheduled').count()
        
        # This month's announcements
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month = Announcement.query.filter(
            Announcement.created_at >= current_month
        ).count()
        
        # Featured announcements
        featured = Announcement.query.filter_by(is_featured=True).count()
        
        # Pinned announcements
        pinned = Announcement.query.filter_by(is_pinned=True).count()
        
        # Expired announcements
        expired = Announcement.query.filter(
            Announcement.expiry_date < datetime.utcnow()
        ).count()
        
        # Active announcements (published and not expired)
        active = Announcement.query.filter(
            Announcement.status == 'published',
            db.or_(
                Announcement.expiry_date.is_(None),
                Announcement.expiry_date > datetime.utcnow()
            )
        ).count()
        
        return {
            'total_announcements': total_announcements,
            'published': published,
            'draft': draft,
            'scheduled': scheduled,
            'this_month': this_month,
            'featured': featured,
            'pinned': pinned,
            'expired': expired,
            'active': active
        }
        
    except Exception as e:
        print(f"Error getting announcement stats: {e}")
        return {
            'total_announcements': 0,
            'published': 0,
            'draft': 0,
            'scheduled': 0,
            'this_month': 0,
            'featured': 0,
            'pinned': 0,
            'expired': 0,
            'active': 0
        }

def export_blotters(blotters, format_type):
    """Export blotter records to CSV or Excel"""
    try:
        import io
        import csv
        from flask import make_response
        
        if format_type == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow([
                'Case Number', 'Complainant', 'Respondent', 'Incident Date', 'Incident Time',
                'Incident Type', 'Location', 'Status', 'Priority', 'Reported By',
                'Description', 'Created Date'
            ])
            
            # Write data
            for blotter in blotters:
                writer.writerow([
                    blotter.case_number,
                    blotter.complainant_name,
                    blotter.respondent_name,
                    blotter.incident_date.strftime('%Y-%m-%d') if blotter.incident_date else '',
                    blotter.incident_time.strftime('%H:%M') if blotter.incident_time else '',
                    blotter.formatted_incident_type,
                    blotter.incident_place or '',
                    blotter.formatted_status,
                    blotter.priority.title(),
                    blotter.reported_by or '',
                    blotter.incident_description or '',
                    blotter.created_at.strftime('%Y-%m-%d %H:%M')
                ])
            
            # Create response
            response = make_response(output.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=blotter_records.csv'
            response.headers['Content-Type'] = 'text/csv'
            return response
            
        else:  # Excel format - fallback to CSV
            return export_blotters(blotters, 'csv')
                
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error exporting blotters: {str(e)}'
        }), 500

# ========================================
# CERTIFICATE PAYMENT ROUTES
# ========================================

@clerk_bp.route('/certificate/<int:certificate_id>/payment')
@clerk_required
def certificate_payment(certificate_id):
    """Show payment processing page for a specific certificate"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Ensure certificate can proceed to payment
        if not certificate.can_proceed_to_payment:
            flash('This certificate is not ready for payment processing.', 'error')
            return redirect(url_for('admin.certificates'))
        
        return render_template('clerk/certificate-payment.html', certificate=certificate)
        
    except Exception as e:
        flash(f'Error loading payment page: {str(e)}', 'error')
        return redirect(url_for('admin.certificates'))

@clerk_bp.route('/api/certificate/<int:certificate_id>/reject', methods=['POST'])
@clerk_required
def reject_certificate_api(certificate_id):
    """Reject a certificate with reason"""
    try:
        data = request.get_json()
        reason = data.get('reason', '').strip()
        
        if not reason:
            return jsonify({
                'success': False,
                'message': 'Rejection reason is required'
            }), 400
        
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Reject the certificate
        certificate.reject(reason, session.get('user_id'))
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate rejected successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error rejecting certificate: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate/<int:certificate_id>', methods=['GET'])
@clerk_required
def get_certificate_api(certificate_id):
    """Get certificate details"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Format certificate type for display
        certificate_type_names = {
            'barangay_clearance': 'Barangay Clearance',
            'certificate_of_indigency': 'Certificate of Indigency',
            'business_permit': 'Business Permit',
            'certificate_of_residency': 'Certificate of Residency',
            'cedula': 'Cedula',
            'tribal_membership': 'Tribal Membership'
        }
        
        return jsonify({
            'success': True,
            'certificate': {
                'id': certificate.id,
                'certificate_number': certificate.certificate_number,
                'certificate_type': certificate.certificate_type,
                'certificate_type_display': certificate_type_names.get(certificate.certificate_type, certificate.certificate_type.replace('_', ' ').title()),
                'purpose': certificate.purpose,
                'status': certificate.status,
                'payment_status': certificate.payment_status,
                'fee': float(certificate.fee) if certificate.fee else 0,
                'request_date': certificate.request_date.isoformat() if certificate.request_date else None,
                'processed_date': certificate.processed_date.isoformat() if certificate.processed_date else None,
                'resident_name': certificate.resident.full_name,
                'resident_email': certificate.resident.email,
                'resident_phone': certificate.resident.phone,
                'notes': certificate.notes,
                'rejection_reason': certificate.rejection_reason
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting certificate: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate/<int:certificate_id>', methods=['PUT'])
@clerk_required
def update_certificate_api(certificate_id):
    """Update certificate details"""
    try:
        data = request.get_json()
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Update allowed fields
        if 'purpose' in data:
            certificate.purpose = data['purpose']
        if 'status' in data:
            certificate.status = data['status']
        if 'payment_status' in data:
            certificate.payment_status = data['payment_status']
        if 'notes' in data:
            certificate.notes = data['notes']
        
        # Update processed info if status changes
        if 'status' in data and data['status'] in ['approved', 'rejected', 'processing']:
            certificate.processed_by = session.get('user_id')
            certificate.processed_date = datetime.utcnow()
            
            # Generate certificate number if approved
            if data['status'] == 'approved' and not certificate.certificate_number:
                certificate.certificate_number = certificate.generate_certificate_number()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate updated successfully',
            'certificate': certificate.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating certificate: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate/<int:certificate_id>/complete', methods=['POST'])
@clerk_required
def complete_certificate_api(certificate_id):
    """Mark certificate as completed and create payment record"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Check if certificate can be completed
        if certificate.status != 'approved':
            return jsonify({
                'success': False,
                'message': 'Only approved certificates can be marked as completed'
            }), 400
        
        # Mark certificate as completed (this will auto-create payment)
        certificate.complete(session.get('user_id'))
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate marked as completed',
            'certificate': certificate.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error completing certificate: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate/<int:certificate_id>/payment', methods=['PUT'])
@clerk_required
def update_certificate_payment_api(certificate_id):
    """Update certificate payment status and sync to database"""
    try:
        data = request.get_json()
        certificate = Certificate.query.get_or_404(certificate_id)
        payment_method = data.get('payment_method', 'cash')  # Default to cash
        
        # Update payment status
        if 'payment_status' in data:
            certificate.payment_status = data['payment_status']
            
            # If marked as paid, create or update payment record
            if data['payment_status'] == 'paid':
                certificate.payment_date = datetime.utcnow()
                
                # Try to set payment_completed field (may not exist in older database)
                try:
                    certificate.payment_completed = True
                except AttributeError:
                    pass  # Field doesn't exist in database yet
                
                # Find existing payment record or create new one
                existing_payment = Payment.query.filter_by(certificate_id=certificate_id).first()
                
                if existing_payment:
                    # Update existing payment record
                    existing_payment.payment_status = 'paid'
                    existing_payment.payment_method = payment_method
                    existing_payment.payment_date = datetime.utcnow()
                    existing_payment.processed_by = session.get('user_id')
                    existing_payment.processed_at = datetime.utcnow()
                    existing_payment.verification_status = 'verified'
                    existing_payment.receipt_issued = True
                    existing_payment.receipt_issued_at = datetime.utcnow()
                    existing_payment.receipt_issued_by = session.get('user_id')
                    
                    # Generate receipt number if not exists
                    if not existing_payment.receipt_number:
                        try:
                            existing_payment.receipt_number = existing_payment.generate_receipt_number()
                        except Exception as receipt_error:
                            print(f"Receipt generation error: {receipt_error}")
                            existing_payment.receipt_number = f"RCP-{certificate_id}-{int(datetime.utcnow().timestamp())}"
                else:
                    # Create new payment record
                    payment = Payment(
                        resident_id=certificate.resident_id,
                        certificate_id=certificate.id,
                        payer_name=certificate.resident.full_name,
                        payer_email=certificate.resident.email or '',
                        payer_phone=certificate.resident.phone or '',
                        service_type=certificate.certificate_type,
                        service_description=f"{certificate.certificate_type.replace('_', ' ').title()} - {certificate.purpose}",
                        amount=float(certificate.fee) if certificate.fee else 0.0,
                        payment_method=payment_method,
                        payment_status='paid',
                        payment_date=datetime.utcnow(),
                        base_fee=float(certificate.fee) if certificate.fee else 0.0,
                        payment_category='service_fee',
                        priority='normal',
                        notes=f'Payment for certificate #{certificate.certificate_number or certificate.id}',
                        created_by=session.get('user_id'),
                        processed_by=session.get('user_id'),
                        processed_at=datetime.utcnow(),
                        verification_status='verified',
                        receipt_issued=True,
                        receipt_issued_at=datetime.utcnow(),
                        receipt_issued_by=session.get('user_id'),
                        is_certificate_payment=True
                    )
                    
                    # Generate receipt number
                    try:
                        payment.receipt_number = payment.generate_receipt_number()
                    except Exception as receipt_error:
                        print(f"Receipt generation error: {receipt_error}")
                        payment.receipt_number = f"RCP-{certificate_id}-{int(datetime.utcnow().timestamp())}"
                    
                    db.session.add(payment)
                
                # Auto-move to payment list if certificate is completed
                if certificate.status == 'completed':
                    try:
                        certificate.moved_to_payment_list = True
                        certificate.moved_to_payment_list_date = datetime.utcnow()
                        
                        # Update payment record for payment list
                        payment_record = existing_payment or payment
                        if hasattr(payment_record, 'moved_to_payment_list'):
                            payment_record.moved_to_payment_list = True
                            payment_record.moved_to_payment_list_date = datetime.utcnow()
                    except AttributeError:
                        pass  # Payment list fields don't exist yet
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment processed and synced to database successfully',
            'certificate': certificate.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Payment processing error: {str(e)}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full traceback
        return jsonify({
            'success': False,
            'message': f'Error processing payment: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate/<int:certificate_id>/move-to-payment-list', methods=['POST'])
@clerk_required
def move_certificate_to_payment_list_api(certificate_id):
    """Copy completed and paid certificate to payment list for logging"""
    try:
        certificate = Certificate.query.get_or_404(certificate_id)
        
        # Check if certificate is eligible to copy to payment list
        if certificate.status != 'completed':
            return jsonify({
                'success': False,
                'message': 'Certificate must be completed to copy to payment list'
            }), 400
            
        if certificate.payment_status != 'paid':
            return jsonify({
                'success': False,
                'message': 'Certificate payment must be marked as paid to copy to payment list'
            }), 400
        
        # Check if already copied to avoid duplicates
        if certificate.moved_to_payment_list:
            return jsonify({
                'success': True,
                'message': 'Certificate already copied to payment list',
                'certificate': certificate.to_dict()
            })
        
        # Create or update payment record for payment list logging
        payment = certificate.latest_payment
        if not payment:
            # Create new payment record for logging
            payment = Payment(
                resident_id=certificate.resident_id,
                certificate_id=certificate.id,
                payer_name=certificate.resident.full_name if certificate.resident else 'Unknown',
                payer_email=certificate.resident.email if certificate.resident else '',
                payer_phone=certificate.resident.phone if certificate.resident else '',
                service_type=certificate.certificate_type,
                service_description=f"{certificate.certificate_type.replace('_', ' ').title()} - {certificate.purpose}",
                amount=float(certificate.fee) if certificate.fee else 0.0,
                payment_method='completed_certificate',  # Mark as completed certificate
                payment_status='paid',  # Already paid
                payment_date=datetime.utcnow(),
                base_fee=float(certificate.fee) if certificate.fee else 0.0,
                payment_category='service_fee',
                priority='normal',
                notes=f'Auto-generated payment log for completed certificate #{certificate.certificate_number}',
                created_by=session.get('user_id', 1),
                processed_by=session.get('user_id', 1),
                processed_at=datetime.utcnow(),
                is_certificate_payment=True,
                moved_to_payment_list=True,
                moved_to_payment_list_date=datetime.utcnow()
            )
            payment.receipt_number = payment.generate_receipt_number()
            db.session.add(payment)
        else:
            # Update existing payment to move to payment list
            payment.moved_to_payment_list = True
            payment.moved_to_payment_list_date = datetime.utcnow()
            if payment.payment_status != 'paid':
                payment.payment_status = 'paid'
                payment.payment_date = datetime.utcnow()
                payment.processed_by = session.get('user_id', 1)
                payment.processed_at = datetime.utcnow()
            if not payment.receipt_number:
                payment.receipt_number = payment.generate_receipt_number()
        
        # Mark certificate as copied to payment list (but keep it in certificates)
        certificate.moved_to_payment_list = True
        certificate.moved_to_payment_list_date = datetime.utcnow()
        certificate.payment_completed = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate successfully copied to payment list for logging',
            'certificate': certificate.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error copying certificate to payment list: {str(e)}'
        }), 500

@clerk_bp.route('/api/sync-payment-list', methods=['POST'])
@clerk_required
def sync_payment_list_api():
    """Sync all completed and paid certificates to payment list"""
    try:
        # Find certificates that are both completed and paid but not moved yet
        certificates_to_sync = Certificate.query.filter_by(
            status='completed', 
            payment_status='paid',
            moved_to_payment_list=False
        ).all()
        
        count = 0
        for cert in certificates_to_sync:
            # Create or update payment record for logging
            payment = cert.latest_payment
            if not payment:
                # Create new payment record for logging
                payment = Payment(
                    resident_id=cert.resident_id,
                    certificate_id=cert.id,
                    payer_name=cert.resident.full_name if cert.resident else 'Unknown',
                    payer_email=cert.resident.email if cert.resident else '',
                    payer_phone=cert.resident.phone if cert.resident else '',
                    service_type=cert.certificate_type,
                    service_description=f"{cert.certificate_type.replace('_', ' ').title()} - {cert.purpose}",
                    amount=float(cert.fee) if cert.fee else 0.0,
                    payment_method='completed_certificate',
                    payment_status='paid',
                    payment_date=datetime.utcnow(),
                    base_fee=float(cert.fee) if cert.fee else 0.0,
                    payment_category='service_fee',
                    priority='normal',
                    notes=f'Auto-generated payment log for completed certificate #{cert.certificate_number}',
                    created_by=session.get('user_id', 1),
                    processed_by=session.get('user_id', 1),
                    processed_at=datetime.utcnow(),
                    is_certificate_payment=True,
                    moved_to_payment_list=True,
                    moved_to_payment_list_date=datetime.utcnow()
                )
                payment.receipt_number = payment.generate_receipt_number()
                db.session.add(payment)
            else:
                # Update existing payment to move to payment list
                payment.moved_to_payment_list = True
                payment.moved_to_payment_list_date = datetime.utcnow()
                if payment.payment_status != 'paid':
                    payment.payment_status = 'paid'
                    payment.payment_date = datetime.utcnow()
                    payment.processed_by = session.get('user_id', 1)
                    payment.processed_at = datetime.utcnow()
                if not payment.receipt_number:
                    payment.receipt_number = payment.generate_receipt_number()
            
            # Mark certificate as moved to payment list
            cert.moved_to_payment_list = True 
            cert.moved_to_payment_list_date = datetime.utcnow()
            cert.payment_completed = True
            count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully synced {count} certificates to payment list',
            'count': count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error syncing payment list: {str(e)}'
        }), 500

@clerk_bp.route('/api/residents', methods=['GET'])
@clerk_required
def get_residents_api():
    """Get list of approved residents for dropdowns"""
    try:
        residents = Resident.query.filter_by(status='approved').order_by(Resident.first_name, Resident.last_name).all()
        
        residents_data = [{
            'id': resident.id,
            'full_name': resident.full_name,
            'first_name': resident.first_name,
            'last_name': resident.last_name,
            'email': resident.email,
            'phone': resident.phone
        } for resident in residents]
        
        return jsonify({
            'success': True,
            'residents': residents_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting residents: {str(e)}'
        }), 500

# Certificate Types Management API Endpoints
@clerk_bp.route('/api/certificate-types', methods=['GET'])
@clerk_required
def get_certificate_types():
    """Get all certificate types"""
    try:
        from models import CertificateType
        
        certificate_types = CertificateType.query.order_by(CertificateType.name).all()
        
        types_data = [{
            'id': cert_type.id,
            'name': cert_type.name,
            'code': cert_type.code,
            'description': cert_type.description,
            'fee': float(cert_type.fee) if cert_type.fee else 0.0,
            'formatted_fee': cert_type.formatted_fee,
            'is_active': cert_type.is_active,
            'is_available_online': cert_type.is_available_online,
            'requires_approval': cert_type.requires_approval,
            'processing_days': cert_type.processing_days,
            'requirements': cert_type.requirements
        } for cert_type in certificate_types]
        
        return jsonify({
            'success': True,
            'certificate_types': types_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting certificate types: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate-types', methods=['POST'])
@clerk_required
def create_certificate_type():
    """Create new certificate type"""
    try:
        from models import CertificateType
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('code'):
            return jsonify({
                'success': False,
                'message': 'Name and code are required'
            }), 400
        
        # Check if code already exists
        existing = CertificateType.query.filter_by(code=data['code']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Certificate type code already exists'
            }), 400
        
        # Create new certificate type
        cert_type = CertificateType(
            name=data['name'],
            code=data['code'],
            description=data.get('description', ''),
            fee=Decimal(str(data.get('fee', 0))),
            is_active=data.get('is_active', True),
            is_available_online=data.get('is_available_online', True),
            requires_approval=data.get('requires_approval', True),
            processing_days=data.get('processing_days', 3),
            requirements=data.get('requirements', '[]')
        )
        
        db.session.add(cert_type)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate type created successfully',
            'certificate_type': cert_type.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating certificate type: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate-types/<int:type_id>', methods=['PUT'])
@clerk_required
def update_certificate_type(type_id):
    """Update certificate type"""
    try:
        from models import CertificateType
        
        cert_type = CertificateType.query.get_or_404(type_id)
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            cert_type.name = data['name']
        if 'description' in data:
            cert_type.description = data['description']
        if 'fee' in data:
            cert_type.fee = Decimal(str(data['fee']))
        if 'is_active' in data:
            cert_type.is_active = data['is_active']
        if 'is_available_online' in data:
            cert_type.is_available_online = data['is_available_online']
        if 'requires_approval' in data:
            cert_type.requires_approval = data['requires_approval']
        if 'processing_days' in data:
            cert_type.processing_days = data['processing_days']
        if 'requirements' in data:
            cert_type.requirements = data['requirements']
        
        cert_type.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate type updated successfully',
            'certificate_type': cert_type.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating certificate type: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate-types/<int:type_id>', methods=['DELETE'])
@clerk_required
def delete_certificate_type(type_id):
    """Delete certificate type"""
    try:
        from models import CertificateType
        
        cert_type = CertificateType.query.get_or_404(type_id)
        
        # Check if certificate type is being used
        certificates_count = Certificate.query.filter_by(certificate_type=cert_type.code).count()
        if certificates_count > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete certificate type. It is being used by {certificates_count} certificates.'
            }), 400
        
        db.session.delete(cert_type)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Certificate type deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting certificate type: {str(e)}'
        }), 500

@clerk_bp.route('/api/certificate-types/sync', methods=['POST'])
@clerk_required
def sync_certificate_types():
    """Initialize or sync certificate types with default values"""
    try:
        from models import CertificateType
        
        default_types = CertificateType.get_default_types()
        created_count = 0
        updated_count = 0
        
        for type_data in default_types:
            existing = CertificateType.query.filter_by(code=type_data['code']).first()
            
            if existing:
                # Update existing type with new fee if different
                if float(existing.fee) != type_data['fee']:
                    existing.fee = Decimal(str(type_data['fee']))
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
            else:
                # Create new type
                cert_type = CertificateType(
                    name=type_data['name'],
                    code=type_data['code'],
                    description=type_data['description'],
                    fee=Decimal(str(type_data['fee'])),
                    processing_days=type_data['processing_days'],
                    requirements=type_data['requirements']
                )
                db.session.add(cert_type)
                created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Sync completed. Created: {created_count}, Updated: {updated_count}',
            'created': created_count,
            'updated': updated_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error syncing certificate types: {str(e)}'
        }), 500

# System Settings API Endpoints
@clerk_bp.route('/api/system-settings', methods=['GET'])
@clerk_required
def get_system_settings():
    """Get system settings"""
    try:
        from models import SystemSettings
        settings = SystemSettings.get_settings()
        return jsonify({
            'success': True,
            'settings': settings.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading system settings: {str(e)}'
        }), 500

@clerk_bp.route('/api/system-settings', methods=['POST'])
@clerk_required
def update_system_settings():
    """Update system settings"""
    try:
        from models import SystemSettings
        data = request.get_json()
        
        settings = SystemSettings.get_settings()
        
        # Update fields if provided in request
        if 'system_name' in data:
            settings.system_name = data['system_name']
        if 'system_description' in data:
            settings.system_description = data['system_description']
        if 'timezone' in data:
            settings.timezone = data['timezone']
        if 'language' in data:
            settings.language = data['language']
        if 'date_format' in data:
            settings.date_format = data['date_format']
        if 'currency' in data:
            settings.currency = data['currency']
        if 'maintenance_mode' in data:
            settings.maintenance_mode = bool(data['maintenance_mode'])
        if 'registration_enabled' in data:
            settings.registration_enabled = bool(data['registration_enabled'])
        if 'email_notifications' in data:
            settings.email_notifications = bool(data['email_notifications'])
        if 'sms_notifications' in data:
            settings.sms_notifications = bool(data['sms_notifications'])
        if 'max_file_size_mb' in data:
            settings.max_file_size_mb = int(data['max_file_size_mb'])
        if 'allowed_file_types' in data:
            if isinstance(data['allowed_file_types'], list):
                settings.allowed_file_types = ','.join(data['allowed_file_types'])
            else:
                settings.allowed_file_types = str(data['allowed_file_types'])
        if 'session_timeout_minutes' in data:
            settings.session_timeout_minutes = int(data['session_timeout_minutes'])
        if 'password_min_length' in data:
            settings.password_min_length = int(data['password_min_length'])
        if 'password_expiry_days' in data:
            settings.password_expiry_days = int(data['password_expiry_days'])
        if 'failed_login_attempts' in data:
            settings.failed_login_attempts = int(data['failed_login_attempts'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'System settings updated successfully',
            'settings': settings.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating system settings: {str(e)}'
        }), 500

# Barangay Information API Endpoints
@clerk_bp.route('/api/barangay-info', methods=['GET'])
@clerk_required
def get_barangay_info():
    """Get barangay information"""
    try:
        from models import BarangayInfo
        info = BarangayInfo.get_info()
        return jsonify({
            'success': True,
            'barangay_info': info.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading barangay information: {str(e)}'
        }), 500

@clerk_bp.route('/api/barangay-info', methods=['POST'])
@clerk_required
def update_barangay_info():
    """Update barangay information"""
    try:
        from models import BarangayInfo
        data = request.get_json()
        
        info = BarangayInfo.get_info()
        
        # Update fields if provided in request
        if 'barangay_name' in data:
            info.barangay_name = data['barangay_name']
        if 'municipality' in data:
            info.municipality = data['municipality']
        if 'province' in data:
            info.province = data['province']
        if 'region' in data:
            info.region = data['region']
        if 'zip_code' in data:
            info.zip_code = data['zip_code']
        if 'street_address' in data:
            info.street_address = data['street_address']
        if 'barangay_hall_address' in data:
            info.barangay_hall_address = data['barangay_hall_address']
        if 'phone_number' in data:
            info.phone_number = data['phone_number']
        if 'mobile_number' in data:
            info.mobile_number = data['mobile_number']
        if 'fax_number' in data:
            info.fax_number = data['fax_number']
        if 'email_address' in data:
            info.email_address = data['email_address']
        if 'website' in data:
            info.website = data['website']
        if 'facebook_page' in data:
            info.facebook_page = data['facebook_page']
        if 'captain_name' in data:
            info.captain_name = data['captain_name']
        if 'captain_term_start' in data:
            if data['captain_term_start']:
                info.captain_term_start = datetime.strptime(data['captain_term_start'], '%Y-%m-%d').date()
        if 'captain_term_end' in data:
            if data['captain_term_end']:
                info.captain_term_end = datetime.strptime(data['captain_term_end'], '%Y-%m-%d').date()
        if 'secretary_name' in data:
            info.secretary_name = data['secretary_name']
        if 'treasurer_name' in data:
            info.treasurer_name = data['treasurer_name']
        if 'office_hours' in data:
            info.office_hours = data['office_hours']
        if 'service_days' in data:
            info.service_days = data['service_days']
        if 'emergency_hotline' in data:
            info.emergency_hotline = data['emergency_hotline']
        if 'total_population' in data:
            info.total_population = int(data['total_population']) if data['total_population'] else None
        if 'total_households' in data:
            info.total_households = int(data['total_households']) if data['total_households'] else None
        if 'total_area_hectares' in data:
            info.total_area_hectares = Decimal(str(data['total_area_hectares'])) if data['total_area_hectares'] else None
        if 'mission_statement' in data:
            info.mission_statement = data['mission_statement']
        if 'vision_statement' in data:
            info.vision_statement = data['vision_statement']
        if 'brief_history' in data:
            info.brief_history = data['brief_history']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Barangay information updated successfully',
            'barangay_info': info.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating barangay information: {str(e)}'
        }), 500

# User Management API Endpoints
@clerk_bp.route('/api/users', methods=['GET'])
@clerk_required
def get_users():
    """Get all users including approved residents"""
    try:
        # Get all users sorted by role priority (admin/clerk at top, then residents)
        users = User.query.order_by(
            db.case(
                (User.role == 'super_admin', 1),
                (User.role == 'admin', 2),
                (User.role == 'clerk', 3),
                (User.role == 'resident', 4),
                else_=5
            ),
            User.name
        ).all()
        
        users_data = []
        for user in users:
            # Filter out pending residents
            if user.role == 'resident' and user.resident_profile:
                if user.resident_profile.status == 'pending':
                    continue
            
            users_data.append({
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'last_login': None  # You can add last_login field to User model if needed
            })
        
        return jsonify({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading users: {str(e)}'
        }), 500

@clerk_bp.route('/api/users', methods=['POST'])
@clerk_required
def create_user():
    """Create a new admin user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'username', 'email', 'password', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Field {field} is required'
                }), 400
        
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username or email already exists'
            }), 400
        
        # Validate role
        valid_roles = ['admin', 'clerk', 'super_admin']
        if data['role'] not in valid_roles:
            return jsonify({
                'success': False,
                'message': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
            }), 400
        
        # Create new user
        user = User(
            name=data['name'],
            username=data['username'],
            email=data['email'],
            role=data['role'],
            is_active=data.get('is_active', True),
            pending_approval=False  # Admin-created users don't need approval
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating user: {str(e)}'
        }), 500

@clerk_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@clerk_required
def update_user(user_id):
    """Update an existing user"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Don't allow editing super_admin users unless current user is super_admin
        current_user_role = session.get('role')
        if user.role == 'super_admin' and current_user_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only super admins can edit super admin users'
            }), 403
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists'
                }), 400
            user.email = data['email']
        if 'role' in data:
            valid_roles = ['admin', 'clerk', 'super_admin']
            if data['role'] not in valid_roles:
                return jsonify({
                    'success': False,
                    'message': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
                }), 400
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'updated_at': user.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating user: {str(e)}'
        }), 500

@clerk_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@clerk_required
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Don't allow deleting super_admin users unless current user is super_admin
        current_user_role = session.get('role')
        if user.role == 'super_admin' and current_user_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only super admins can delete super admin users'
            }), 403
        
        # Don't allow users to delete themselves
        current_user_id = session.get('user_id')
        if user.id == current_user_id:
            return jsonify({
                'success': False,
                'message': 'You cannot delete your own account'
            }), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting user: {str(e)}'
        }), 500


# ================== PUROK/SITIO MANAGEMENT API ENDPOINTS ==================

@clerk_bp.route('/api/purok', methods=['GET'])
@clerk_required
def get_purok_list():
    """Get list of all purok/sitio"""
    try:
        puroks = PurokInfo.query.filter_by(is_active=True).order_by(PurokInfo.name).all()
        purok_data = [purok.to_dict() for purok in puroks]
        
        return jsonify({
            'success': True,
            'purok': purok_data,
            'message': f'Retrieved {len(purok_data)} purok/sitio records'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving purok data: {str(e)}'
        }), 500

@clerk_bp.route('/api/purok/<int:purok_id>', methods=['GET'])
@clerk_required
def get_purok(purok_id):
    """Get specific purok/sitio by ID"""
    try:
        purok = PurokInfo.query.get_or_404(purok_id)
        return jsonify({
            'success': True,
            'purok': purok.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving purok: {str(e)}'
        }), 404

@clerk_bp.route('/api/purok', methods=['POST'])
@clerk_required
def create_purok():
    """Create new purok/sitio"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'Purok/Sitio name is required'
            }), 400
        
        # Check if name already exists
        existing = PurokInfo.query.filter_by(name=data.get('name')).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'A purok/sitio with this name already exists'
            }), 400
        
        # Create new purok
        purok = PurokInfo(
            name=data.get('name'),
            type=data.get('type', 'Purok'),
            description=data.get('description'),
            leader_name=data.get('leader_name'),
            leader_contact=data.get('leader_contact'),
            leader_address=data.get('leader_address'),
            boundaries=data.get('boundaries'),
            area_hectares=data.get('area_hectares'),
            population_count=data.get('population_count', 0),
            household_count=data.get('household_count', 0),
            landmark=data.get('landmark'),
            zip_code=data.get('zip_code'),
            coordinates_lat=data.get('coordinates_lat'),
            coordinates_lng=data.get('coordinates_lng'),
            created_by=session.get('user_id'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(purok)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{purok.type} "{purok.name}" created successfully',
            'purok': purok.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating purok: {str(e)}'
        }), 500

@clerk_bp.route('/api/purok/<int:purok_id>', methods=['PUT'])
@clerk_required
def update_purok(purok_id):
    """Update existing purok/sitio"""
    try:
        purok = PurokInfo.query.get_or_404(purok_id)
        data = request.get_json()
        
        # Check if new name conflicts with existing records (excluding current record)
        if data.get('name') and data.get('name') != purok.name:
            existing = PurokInfo.query.filter(
                PurokInfo.name == data.get('name'),
                PurokInfo.id != purok_id
            ).first()
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'A purok/sitio with this name already exists'
                }), 400
        
        # Update fields
        purok.name = data.get('name', purok.name)
        purok.type = data.get('type', purok.type)
        purok.description = data.get('description', purok.description)
        purok.leader_name = data.get('leader_name', purok.leader_name)
        purok.leader_contact = data.get('leader_contact', purok.leader_contact)
        purok.leader_address = data.get('leader_address', purok.leader_address)
        purok.boundaries = data.get('boundaries', purok.boundaries)
        purok.area_hectares = data.get('area_hectares', purok.area_hectares)
        purok.population_count = data.get('population_count', purok.population_count)
        purok.household_count = data.get('household_count', purok.household_count)
        purok.landmark = data.get('landmark', purok.landmark)
        purok.zip_code = data.get('zip_code', purok.zip_code)
        purok.coordinates_lat = data.get('coordinates_lat', purok.coordinates_lat)
        purok.coordinates_lng = data.get('coordinates_lng', purok.coordinates_lng)
        purok.is_active = data.get('is_active', purok.is_active)
        purok.updated_by = session.get('user_id')
        purok.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{purok.type} "{purok.name}" updated successfully',
            'purok': purok.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating purok: {str(e)}'
        }), 500

@clerk_bp.route('/api/purok/<int:purok_id>', methods=['DELETE'])
@clerk_required
def delete_purok(purok_id):
    """Delete (soft delete) purok/sitio"""
    try:
        purok = PurokInfo.query.get_or_404(purok_id)
        
        # Soft delete by setting is_active to False
        purok.is_active = False
        purok.updated_by = session.get('user_id')
        purok.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{purok.type} "{purok.name}" deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting purok: {str(e)}'
        }), 500

@clerk_bp.route('/api/purok/<int:purok_id>/toggle-status', methods=['POST'])
@clerk_required
def toggle_purok_status(purok_id):
    """Toggle purok/sitio active status"""
    try:
        purok = PurokInfo.query.get_or_404(purok_id)
        
        purok.is_active = not purok.is_active
        purok.updated_by = session.get('user_id')
        purok.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        status = "activated" if purok.is_active else "deactivated"
        return jsonify({
            'success': True,
            'message': f'{purok.type} "{purok.name}" {status} successfully',
            'purok': purok.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error toggling purok status: {str(e)}'
        }), 500

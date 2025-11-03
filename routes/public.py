from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid
from datetime import datetime
from . import public_bp
from models import db, Resident, Announcement, Official, User, Certificate, CertificateType, BarangayInfo, ContactMessage, PurokInfo
from utils import validate_form_data, validate_email, validate_password, success_response, error_response

# File upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_type='documents'):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        
        # Determine upload path
        upload_folder = os.path.join(current_app.static_folder, 'uploads', upload_type)
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        return unique_filename
    return None

def validate_signup_form(form_data):
    """Validate signup form data"""
    errors = {}
    
    # Required fields validation
    required_fields = ['firstName', 'lastName', 'email', 'phone', 'birthDate', 
                      'birthPlace', 'gender', 'civilStatus', 'houseNumber', 
                      'street', 'purok', 'username', 'password', 'confirmPassword']
    
    for field in required_fields:
        if not form_data.get(field) or form_data.get(field).strip() == '':
            field_names = {
                'firstName': 'First Name',
                'lastName': 'Last Name', 
                'birthDate': 'Birth Date',
                'birthPlace': 'Birth Place',
                'civilStatus': 'Civil Status',
                'houseNumber': 'House Number',
                'confirmPassword': 'Confirm Password'
            }
            field_name = field_names.get(field, field.title())
            errors[field] = f'{field_name} is required'
    
    # Email validation
    email = form_data.get('email', '').strip()
    if email:
        if '@' not in email or '.' not in email.split('@')[-1]:
            errors['email'] = 'Please enter a valid email address'
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors['email'] = 'Email address already registered'
    
    # Username validation
    username = form_data.get('username', '').strip()
    if username:
        if len(username) < 4 or len(username) > 20:
            errors['username'] = 'Username must be 4-20 characters long'
        if User.query.filter_by(username=username).first():
            errors['username'] = 'Username already taken'
    
    # Password validation
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirmPassword', '')
    if password:
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if password != confirm_password:
            errors['confirmPassword'] = 'Passwords do not match'
    
    # Age validation (must be at least 18)
    birth_date = form_data.get('birthDate')
    if birth_date:
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            today = datetime.now().date()
            age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
            if age < 18:
                errors['birthDate'] = 'You must be at least 18 years old to register'
        except ValueError:
            errors['birthDate'] = 'Please enter a valid birth date'
    
    # Terms agreement validation
    if not form_data.get('agreeToTerms'):
        errors['agreeToTerms'] = 'You must agree to the terms of service'
    
    return errors

@public_bp.route('/')
def index():
    try:
        # Get current datetime for filtering
        now = datetime.utcnow()
        
        # Get featured announcements (published, not expired, event date hasn't passed)
        featured_announcements = Announcement.query.filter(
            Announcement.is_published == True,
            Announcement.is_featured == True,
            db.or_(
                Announcement.expiry_date.is_(None),
                Announcement.expiry_date > now
            ),
            db.or_(
                Announcement.event_date.is_(None),
                Announcement.event_date >= now.date()
            )
        ).order_by(Announcement.created_at.desc()).limit(3).all()
        
        # Get database stats
        approved_residents_count = Resident.query.filter_by(status='approved').count()
        completed_certificates_count = Certificate.query.filter_by(status='completed').count()
        
        # Get active certificate types for services section
        certificate_types = CertificateType.query.filter_by(is_active=True, is_available_online=True).limit(6).all()
        
        # Get barangay info for contact section
        barangay_info = BarangayInfo.query.first()
        
        # Prepare stats for template
        stats = {
            'approved_residents': approved_residents_count,
            'completed_certificates': completed_certificates_count,
            'total_residents': approved_residents_count,  # For backward compatibility
            'monthly_revenue': '15,240.00'  # Keep for other uses if needed
        }
        
        return render_template('public/index.html', 
                             announcements=featured_announcements,
                             stats=stats,
                             certificate_types=certificate_types,
                             barangay_info=barangay_info)
    except Exception as e:
        # If database is not ready, show page with default data
        print(f"Database not ready: {e}")
        
        # Fallback certificate types
        fallback_certificate_types = [
            {
                'name': 'Barangay Clearance',
                'code': 'barangay_clearance',
                'description': 'Official document certifying residency and good moral character within the barangay.',
                'formatted_fee': '₱50.00',
                'processing_days': 3
            },
            {
                'name': 'Certificate of Residency',
                'code': 'certificate_of_residency',
                'description': 'Certificate proving residency in the barangay.',
                'formatted_fee': '₱30.00',
                'processing_days': 2
            },
            {
                'name': 'Certificate of Indigency',
                'code': 'certificate_of_indigency',
                'description': 'Document certifying the economic status for various assistance programs.',
                'formatted_fee': '₱25.00',
                'processing_days': 5
            },
            {
                'name': 'Business Permit',
                'code': 'business_permit',
                'description': 'Authorization to operate a business within the barangay jurisdiction.',
                'formatted_fee': '₱200.00',
                'processing_days': 7
            },
            {
                'name': 'Health Certificate',
                'code': 'health_certificate',
                'description': 'Health clearance certificate for various purposes.',
                'formatted_fee': '₱100.00',
                'processing_days': 3
            },
            {
                'name': 'Good Moral Character',
                'code': 'good_moral_character',
                'description': 'Certificate of good moral character for employment or other purposes.',
                'formatted_fee': '₱75.00',
                'processing_days': 5
            }
        ]
        
        return render_template('public/index.html', 
                             announcements=[],
                             stats={
                                 'approved_residents': 1234, 
                                 'completed_certificates': 156,
                                 'total_residents': 1234, 
                                 'monthly_revenue': '15,240.00'
                             },
                             certificate_types=fallback_certificate_types,
                             barangay_info=None)

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/services')
def services():
    try:
        # Get active certificate types from database
        certificate_types = CertificateType.query.filter_by(
            is_active=True, 
            is_available_online=True
        ).order_by(CertificateType.name).all()
        
        # Get system settings for registration status
        from models import SystemSettings
        settings_obj = SystemSettings.get_settings()
        system_settings = settings_obj.to_dict()
        
        return render_template('public/services.html', 
                             certificate_types=certificate_types,
                             system_settings=system_settings)
    except Exception as e:
        # Fallback in case of database error
        current_app.logger.error(f"Error loading services: {str(e)}")
        return render_template('public/services.html', 
                             certificate_types=[],
                             system_settings={'registration_enabled': True})

@public_bp.route('/announcements')
def announcements():
    page = request.args.get('page', 1, type=int)
    
    # Get current datetime for comparison
    now = datetime.utcnow()
    
    # Filter announcements: published, not expired, and event date hasn't passed
    announcements = Announcement.query.filter(
        Announcement.is_published == True,
        db.or_(
            Announcement.expiry_date.is_(None),  # No expiry date set
            Announcement.expiry_date > now  # Expiry date is in the future
        ),
        db.or_(
            Announcement.event_date.is_(None),  # No event date (not an event)
            Announcement.event_date >= now.date()  # Event date is today or in the future
        )
    ).order_by(
        Announcement.is_pinned.desc(),  # Pinned announcements first
        Announcement.created_at.desc()  # Then by newest
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('public/announcements.html', announcements=announcements)

@public_bp.route('/officials')
def officials():
    officials = Official.query.filter_by(is_active=True).all()
    return render_template('public/officials.html', officials=officials)

@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')

@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check if registration is enabled
    try:
        from models import SystemSettings
        settings_obj = SystemSettings.get_settings()
        settings = settings_obj.to_dict()
        if not settings.get('registration_enabled', True):
            return render_template('public/registration-closed.html'), 403
    except Exception:
        pass  # Continue if settings check fails
    
    if request.method == 'POST':
        # Handle resident registration
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        # Add more fields as needed
        
        # Validate form data
        if not all([first_name, last_name, email]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('public.register'))
        
        # Create new resident record
        resident = Resident(
            first_name=first_name,
            last_name=last_name,
            email=email,
            status='pending'
        )
        
        db.session.add(resident)
        db.session.commit()
        
        flash('Registration submitted successfully! Please wait for approval.', 'success')
        return redirect(url_for('public.index'))
    
    return render_template('public/register.html')

@public_bp.route('/forgot-password')
def forgot_password():
    return render_template('public/forgot-password.html')

@public_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check if registration is enabled
    try:
        from models import SystemSettings
        settings_obj = SystemSettings.get_settings()
        settings = settings_obj.to_dict()
        if not settings.get('registration_enabled', True):
            return render_template('public/registration-closed.html'), 403
    except Exception:
        pass  # Continue if settings check fails
    
    if request.method == 'POST':
        try:
            # Get form data
            form_data = request.form.to_dict()
            
            # Basic validation for required fields
            required_fields = ['firstName', 'lastName', 'email', 'phone', 'birthDate', 
                             'birthPlace', 'gender', 'civilStatus', 'houseNumber', 
                             'purok', 'username', 'password', 'confirmPassword']
            
            errors = {}
            for field in required_fields:
                if not form_data.get(field) or form_data.get(field).strip() == '':
                    errors[field] = f'{field} is required'
            
            # Check password match
            if form_data.get('password') != form_data.get('confirmPassword'):
                errors['confirmPassword'] = 'Passwords do not match'
            
            # Check terms agreement
            if not form_data.get('agreeToTerms'):
                errors['agreeToTerms'] = 'You must agree to the terms'
            
            # Check if email already exists
            existing_email = User.query.filter_by(email=form_data.get('email')).first()
            if existing_email:
                errors['email'] = 'Email address is already registered'
            
            # Check if username already exists
            existing_username = User.query.filter_by(username=form_data.get('username')).first()
            if existing_username:
                errors['username'] = 'Username is already taken'
            
            if errors:
                return jsonify({'success': False, 'errors': errors}), 400
            
            # Handle file uploads
            def save_upload_file(file, folder):
                if file and file.filename != '':
                    # Generate unique filename
                    filename = str(uuid.uuid4()) + '.png'
                    filepath = os.path.join(current_app.root_path, 'static', 'uploads', folder, filename)
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    
                    # Save file
                    file.save(filepath)
                    return f'uploads/{folder}/{filename}'
                return None
            
            # Process file uploads
            profile_picture_path = None
            valid_id_path = None
            proof_of_residency_path = None
            
            if 'profilePicture' in request.files:
                profile_picture_path = save_upload_file(request.files['profilePicture'], 'profiles')
            
            if 'validId' in request.files:
                valid_id_path = save_upload_file(request.files['validId'], 'documents')
                
            if 'proofOfResidency' in request.files:
                proof_of_residency_path = save_upload_file(request.files['proofOfResidency'], 'documents')
            
            # Create user account (simplified)
            from werkzeug.security import generate_password_hash
            
            hashed_password = generate_password_hash(form_data['password'])
            full_name = f"{form_data['firstName']} {form_data.get('middleName', '').strip()} {form_data['lastName']}".strip()
            full_name = ' '.join(full_name.split())
            
            user = User(
                username=form_data['username'],
                email=form_data['email'],
                password=hashed_password,
                name=full_name,
                role='resident',
                is_active=False
            )
            
            db.session.add(user)
            db.session.flush()
            
            # Create resident profile (simplified - no documents for now)
            from datetime import datetime
            birth_date = datetime.strptime(form_data['birthDate'], '%Y-%m-%d').date()
            
            # Get or create purok/sitio
            purok_name = form_data['purok']
            purok = PurokInfo.query.filter_by(name=purok_name).first()
            if not purok:
                # Create new purok if it doesn't exist
                purok = PurokInfo(name=purok_name, type='Purok')
                db.session.add(purok)
                db.session.flush()
            
            resident = Resident(
                user_id=user.id,
                first_name=form_data['firstName'],
                middle_name=form_data.get('middleName', ''),
                last_name=form_data['lastName'],
                suffix=form_data.get('suffix', ''),
                email=form_data['email'],
                phone=form_data['phone'],
                house_number=form_data['houseNumber'],
                sitio_id=purok.id,
                birth_date=birth_date,
                birth_place=form_data['birthPlace'],
                gender=form_data['gender'],
                civil_status=form_data['civilStatus'],
                occupation=form_data.get('occupation', ''),
                is_voter=form_data.get('isVoter') == 'on',
                profile_picture=profile_picture_path,
                valid_id_document=valid_id_path,
                proof_of_residency=proof_of_residency_path,
                status='pending'
            )
            
            db.session.add(resident)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully! Please wait for admin verification before you can log in.',
                'redirect_url': '/login'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'errors': {'general': f'Error: {str(e)}'}}), 500
    
    return render_template('public/signup.html')


@public_bp.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        phone = request.form.get('phone', '').strip()  # Optional field
        
        # Basic validation
        errors = {}
        
        if not name:
            errors['name'] = 'Name is required'
        elif len(name) < 2:
            errors['name'] = 'Name must be at least 2 characters long'
        
        if not email:
            errors['email'] = 'Email is required'
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors['email'] = 'Please enter a valid email address'
        
        if not subject:
            errors['subject'] = 'Subject is required'
        elif len(subject) < 5:
            errors['subject'] = 'Subject must be at least 5 characters long'
        
        if not message:
            errors['message'] = 'Message is required'
        elif len(message) < 10:
            errors['message'] = 'Message must be at least 10 characters long'
        
        # Check for spam (basic check)
        spam_keywords = ['viagra', 'casino', 'lottery', 'prize', 'winner', 'urgent money']
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in spam_keywords):
            errors['message'] = 'Message contains inappropriate content'
        
        if errors:
            return jsonify({
                'success': False, 
                'errors': errors
            }), 400
        
        # Get client information for logging
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        # Create contact message record
        contact_message = ContactMessage(
            name=name,
            email=email,
            phone=phone if phone else None,
            subject=subject,
            message=message,
            status='unread',
            priority='normal',
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Save to database
        db.session.add(contact_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'message_number': contact_message.message_number
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'errors': {'general': 'Sorry, there was an error sending your message. Please try again later.'}
        }), 500


@public_bp.route('/api/puroks', methods=['GET'])
def get_puroks():
    """API endpoint to fetch all active puroks/sitios"""
    try:
        puroks = PurokInfo.query.filter_by(is_active=True).order_by(PurokInfo.name).all()
        purok_list = [{'id': p.id, 'name': p.name, 'type': p.type} for p in puroks]
        return jsonify({'success': True, 'puroks': purok_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@public_bp.route('/signup-success')
def signup_success():
    return render_template('public/signup-success.html')


@public_bp.route('/maintenance')
def maintenance():
    return render_template('public/maintenance.html')

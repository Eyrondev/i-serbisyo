from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pymysql
from dotenv import load_dotenv

# Load environment variables FIRST before importing config
load_dotenv()

from config import config

# Configure PyMySQL to work as MySQLdb replacement
pymysql.install_as_MySQLdb()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Ensure we have a proper secret key for sessions
    if not app.config.get('SECRET_KEY') or app.config['SECRET_KEY'] == 'your-secret-key-change-in-production':
        app.config['SECRET_KEY'] = 'iserbisyo-dev-secret-key-2025-very-secure'
    
    # Additional session configuration
    app.config['SESSION_COOKIE_NAME'] = 'iserbisyo_session'
    app.config['SESSION_COOKIE_DOMAIN'] = None
    app.config['SESSION_COOKIE_PATH'] = '/'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    return app

app = create_app()

# Initialize database
from models import db
db.init_app(app)

# Initialize Flask-Mail
from flask_mail import Mail
mail = Mail(app)

# Import models after db initialization
from models import User, Resident, Certificate, Announcement, Official

# Import blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.clerk import clerk_bp
from routes.resident import resident_bp
from routes.public import public_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(clerk_bp, url_prefix='/clerk')
app.register_blueprint(resident_bp, url_prefix='/residents')
app.register_blueprint(public_bp)

# Template filters
@app.template_filter('number_format')
def number_format_filter(value):
    """Format numbers with comma separators."""
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

# System settings check middleware
@app.before_request
def check_system_settings():
    """Check system settings before processing requests"""
    from models import SystemSettings
    from flask import request, render_template, session
    
    # Skip settings check for static files, admin routes (except login), and API endpoints
    if request.endpoint and (
        request.endpoint.startswith('static') or 
        request.endpoint in ['auth.login', 'auth.logout'] or
        (request.endpoint.startswith('admin') and session.get('user', {}).get('role') in ['admin', 'clerk'])
    ):
        return
    
    try:
        settings_obj = SystemSettings.get_settings()
        settings = settings_obj.to_dict()
        
        # Check maintenance mode
        if settings.get('maintenance_mode', False):
            # Allow admin and clerk users to access the system
            user = session.get('user', {})
            if user.get('role') not in ['admin', 'clerk']:
                return render_template('public/maintenance.html'), 503
        
        # Check registration disabled for signup routes
        if not settings.get('registration_enabled', True):
            if request.endpoint in ['public.signup', 'public.register']:
                return render_template('public/registration-closed.html'), 403
                
    except Exception as e:
        # If there's an error getting settings, continue normally
        print(f"Settings check error: {e}")
        pass

# Context processors for templates
@app.context_processor
def inject_user():
    return dict(current_user=session.get('user'))

@app.context_processor
def inject_notifications():
    """Inject notification counts for sidebar badges"""
    try:
        # Check if user is logged in and is a resident
        if 'user' in session and session.get('user', {}).get('role') == 'resident':
            from models import Resident, Certificate, Announcement
            
            # Get current resident
            user_id = session['user']['id']
            resident = Resident.query.filter_by(user_id=user_id).first()
            
            if resident:
                # Count pending certificates for this resident
                pending_certificates = Certificate.query.filter_by(
                    resident_id=resident.id,
                    status='pending'
                ).count()
                
                # Count only non-expired published announcements
                # Filter out announcements with expiry_date in the past
                from datetime import datetime
                from sqlalchemy import or_
                current_time = datetime.utcnow()
                new_announcements = Announcement.query.filter_by(
                    status='published'
                ).filter(
                    or_(
                        Announcement.expiry_date.is_(None),
                        Announcement.expiry_date > current_time
                    )
                ).count()
                
                return dict(notifications={
                    'pending_certificates': pending_certificates,
                    'new_announcements': new_announcements
                })
        
        # Default values for non-residents or not logged in
        return dict(notifications={
            'pending_certificates': 0,
            'new_announcements': 0
        })
        
    except Exception as e:
        print(f"Notification count error: {e}")
        # Return default values on error
        return dict(notifications={
            'pending_certificates': 0,
            'new_announcements': 0
        })

@app.context_processor
def inject_system_settings():
    """Inject system settings into all templates"""
    try:
        from models import SystemSettings
        settings = SystemSettings.get_settings()
        return dict(system_settings=settings.to_dict())
    except Exception:
        # Return default settings if database is not available
        return dict(system_settings={
            'registration_enabled': True,
            'maintenance_mode': False
        })

@app.context_processor
def inject_footer_data():
    """Inject footer data (certificate types and barangay info) into all templates"""
    try:
        from models import CertificateType, BarangayInfo
        
        # Get certificate types for footer services section
        footer_certificate_types = CertificateType.query.filter_by(
            is_active=True, 
            is_available_online=True
        ).limit(4).all()
        
        # Get barangay information for footer contact section
        footer_barangay_info = BarangayInfo.get_info()
        
        return dict(
            footer_certificate_types=footer_certificate_types,
            footer_barangay_info=footer_barangay_info
        )
    except Exception as e:
        # Return empty data if database is not available
        print(f"Footer data injection error: {e}")
        return dict(
            footer_certificate_types=[],
            footer_barangay_info=None
        )

# Main routes - redirect to public blueprint
@app.route('/')
def index():
    return redirect(url_for('public.index'))

# Authentication handled by auth blueprint

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# CLI commands for database initialization
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    from decimal import Decimal
    
    # Create admin user
    admin_password = generate_password_hash('admin123')
    admin = User(
        username='admin',
        email='admin@iserbisyo.com',
        password=admin_password,
        name='System Administrator',
        role='admin',
        is_active=True,
        pending_approval=False
    )
    
    # Create clerk user
    clerk_password = generate_password_hash('clerk123')
    clerk = User(
        username='clerk',
        email='clerk@iserbisyo.com',
        password=clerk_password,
        name='Barangay Clerk',
        role='clerk',
        is_active=True,
        pending_approval=False
    )
    
    db.session.add(admin)
    db.session.add(clerk)
    db.session.commit()
    
    # Create sample residents
    sample_residents = [
        Resident(
            first_name='Juan', last_name='Cruz', 
            email='juan.cruz@example.com', phone='09123456789',
            house_number='123', street='Main St', purok='1',
            birth_date=datetime(1985, 3, 15).date(),
            gender='male', civil_status='married', 
            occupation='Teacher', status='approved'
        ),
        Resident(
            first_name='Maria', last_name='Santos', 
            email='maria.santos@example.com', phone='09123456790',
            house_number='456', street='Oak Ave', purok='2',
            birth_date=datetime(1990, 7, 22).date(),
            gender='female', civil_status='single', 
            occupation='Nurse', status='approved'
        )
    ]
    
    for resident in sample_residents:
        db.session.add(resident)
    db.session.commit()
    
    # Create sample certificates with fees
    sample_certificates = [
        Certificate(
            resident_id=1, certificate_type='barangay_clearance',
            purpose='Employment requirement', status='claimed',
            fee=Decimal('50.00'), payment_status='paid',
            payment_date=datetime.now(), processed_by=1
        ),
        Certificate(
            resident_id=2, certificate_type='certificate_of_residency',
            purpose='School enrollment', status='ready',
            fee=Decimal('30.00'), payment_status='paid',
            payment_date=datetime.now(), processed_by=1
        ),
        Certificate(
            resident_id=1, certificate_type='indigency_certificate',
            purpose='Medical assistance', status='processing',
            fee=Decimal('25.00'), payment_status='unpaid',
            processed_by=1
        )
    ]
    
    for certificate in sample_certificates:
        db.session.add(certificate)
    db.session.commit()
    
    print('Database seeded with sample users, residents, and certificates!')

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print("📱 Access your app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
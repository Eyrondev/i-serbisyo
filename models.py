from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Database instance will be imported from app.py
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='resident')  # admin, clerk, resident
    is_active = db.Column(db.Boolean, default=True)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # OTP fields for resident login verification
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    otp_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resident_profile = db.relationship('Resident', backref='user', uselist=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def full_name(self):
        """Return the full name for backward compatibility"""
        return self.name
    
    def __repr__(self):
        return f'<User {self.email}>'

class Resident(db.Model):
    __tablename__ = 'residents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Personal Information
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    suffix = db.Column(db.String(10))
    
    # Contact Information
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Address Information
    house_number = db.Column(db.String(20))
    sitio_id = db.Column(db.Integer, db.ForeignKey('purok_info.id'), nullable=True)
    
    # Personal Details
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    civil_status = db.Column(db.String(20))
    occupation = db.Column(db.String(100))
    
    # Document Files
    profile_picture = db.Column(db.String(255))
    valid_id_document = db.Column(db.String(255))
    proof_of_residency = db.Column(db.String(255))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    is_voter = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certificates = db.relationship('Certificate', backref='resident', lazy=True)
    sitio = db.relationship('PurokInfo', backref='residents', lazy=True)
    
    @property
    def full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return ' '.join(parts)
    
    @property
    def full_address(self):
        parts = []
        if self.house_number:
            parts.append(self.house_number)
        if self.sitio:
            parts.append(self.sitio.name)
        return ', '.join(parts) if parts else 'No address provided'
    
    def __repr__(self):
        return f'<Resident {self.full_name}>'

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'), nullable=False)
    
    # Certificate Details
    certificate_type = db.Column(db.String(50), nullable=False)  # barangay_clearance, residency, indigency, etc.
    purpose = db.Column(db.Text)
    
    # Status and Processing
    status = db.Column(db.String(20), default='pending')  # pending, processing, ready, claimed, rejected, approved, completed
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rejection_reason = db.Column(db.Text)  # Reason for rejection
    
    # Dates
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed_date = db.Column(db.DateTime)
    claimed_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)  # When certificate work is completed
    
    # Payment Tracking
    fee = db.Column(db.Numeric(10, 2), default=0.00)
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, pending_payment, paid
    payment_date = db.Column(db.DateTime)
    payment_completed = db.Column(db.Boolean, default=False)  # Track if payment is fully completed
    moved_to_payment_list = db.Column(db.Boolean, default=False)  # Track if moved to payment list
    moved_to_payment_list_date = db.Column(db.DateTime)  # When moved to payment list
    
    # Certificate Number (generated after approval)
    certificate_number = db.Column(db.String(50), unique=True)
    
    # Processing notes
    notes = db.Column(db.Text)
    
    @property
    def can_proceed_to_payment(self):
        """Check if certificate can proceed to payment"""
        return self.status in ['approved', 'processing', 'ready', 'completed'] and self.payment_status in ['unpaid', 'pending_payment']
    
    @property
    def has_payment(self):
        """Check if certificate has associated payment records"""
        return len(self.payment_records) > 0
    
    @property
    def latest_payment(self):
        """Get the latest payment record for this certificate"""
        if self.payment_records:
            return sorted(self.payment_records, key=lambda p: p.created_at, reverse=True)[0]
        return None
    
    @property
    def formatted_fee(self):
        """Format fee with currency"""
        return f"₱{float(self.fee):,.2f}" if self.fee else "₱0.00"
    
    def reject(self, reason, processed_by_id):
        """Reject the certificate with reason"""
        self.status = 'rejected'
        self.rejection_reason = reason
        self.processed_by = processed_by_id
        self.processed_date = datetime.utcnow()
    
    def approve(self, processed_by_id):
        """Approve the certificate"""
        self.status = 'approved'
        self.processed_by = processed_by_id
        self.processed_date = datetime.utcnow()
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
    
    def complete(self, processed_by_id):
        """Mark certificate as completed and create payment record"""
        from models import Payment
        
        self.status = 'completed'
        self.processed_by = processed_by_id
        self.processed_date = datetime.utcnow()
        self.completed_date = datetime.utcnow()
        
        # Generate certificate number if not exists
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
        
        # Create payment record automatically
        if not self.has_payment:
            payment = Payment(
                resident_id=self.resident_id,
                certificate_id=self.id,
                payer_name=self.resident.full_name,
                payer_email=self.resident.email or '',
                payer_phone=self.resident.phone or '',
                service_type=self.certificate_type,
                service_description=f"{self.certificate_type.replace('_', ' ').title()} - {self.purpose}",
                amount=float(self.fee) if self.fee else 0.0,
                payment_method='',  # To be filled when payment is processed
                payment_status='pending',
                base_fee=float(self.fee) if self.fee else 0.0,
                payment_category='service_fee',
                priority='normal',
                notes=f'Auto-generated payment for certificate #{self.certificate_number}',
                created_by=processed_by_id,
                is_certificate_payment=True  # Mark as certificate payment
            )
            
            # Import here to avoid circular imports
            from app import db
            db.session.add(payment)
            
            # Update certificate payment status
            self.payment_status = 'pending_payment'
    
    def mark_payment_completed_and_move_to_list(self, processed_by_id):
        """Mark payment as completed and move to payment list"""
        self.payment_status = 'paid'
        self.payment_date = datetime.utcnow()
        self.payment_completed = True
        self.moved_to_payment_list = True
        self.moved_to_payment_list_date = datetime.utcnow()
        
        # Update associated payment record
        latest_payment = self.latest_payment
        if latest_payment:
            latest_payment.payment_status = 'paid'
            latest_payment.payment_date = datetime.utcnow()
            latest_payment.processed_by = processed_by_id
            latest_payment.moved_to_payment_list = True
            latest_payment.moved_to_payment_list_date = datetime.utcnow()
            
            # Generate receipt number if not exists
            if not latest_payment.receipt_number:
                latest_payment.receipt_number = latest_payment.generate_receipt_number()
    
    @property
    def is_ready_for_payment_list(self):
        """Check if certificate is ready to be moved to payment list"""
        return (self.status == 'completed' and 
                self.payment_completed and 
                self.moved_to_payment_list)
    
    def generate_certificate_number(self):
        """Generate unique certificate number"""
        year = datetime.now().year
        type_code = {
            'barangay_clearance': 'BC',
            'certificate_of_residency': 'CR',
            'certificate_of_indigency': 'CI',
            'business_permit': 'BP',
            'cedula': 'CD'
        }.get(self.certificate_type, 'CT')
        
        count = Certificate.query.filter(
            Certificate.certificate_number.like(f'{type_code}-{year}-%')
        ).count() + 1
        return f'{type_code}-{year}-{count:06d}'
    
    def to_dict(self):
        """Convert certificate to dictionary"""
        return {
            'id': self.id,
            'resident_id': self.resident_id,
            'certificate_type': self.certificate_type,
            'purpose': self.purpose,
            'status': self.status,
            'processed_by': self.processed_by,
            'rejection_reason': self.rejection_reason,
            'request_date': self.request_date.isoformat() if self.request_date else None,
            'processed_date': self.processed_date.isoformat() if self.processed_date else None,
            'claimed_date': self.claimed_date.isoformat() if self.claimed_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'fee': float(self.fee) if self.fee else 0.0,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_completed': self.payment_completed,
            'moved_to_payment_list': self.moved_to_payment_list,
            'moved_to_payment_list_date': self.moved_to_payment_list_date.isoformat() if self.moved_to_payment_list_date else None,
            'certificate_number': self.certificate_number,
            'notes': self.notes,
            'can_proceed_to_payment': self.can_proceed_to_payment,
            'has_payment': self.has_payment,
            'is_ready_for_payment_list': self.is_ready_for_payment_list,
            'formatted_fee': self.formatted_fee,
            'resident_name': self.resident.full_name if self.resident else None
        }
    
    def __repr__(self):
        return f'<Certificate {self.certificate_type} - {self.id}>'

class CertificateType(db.Model):
    __tablename__ = 'certificate_types'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Certificate Type Details
    name = db.Column(db.String(100), nullable=False, unique=True)  # Display name
    code = db.Column(db.String(50), nullable=False, unique=True)  # Internal code (e.g., 'barangay_clearance')
    description = db.Column(db.Text)  # Description of the certificate
    
    # Fee Information
    fee = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    
    # Status and Configuration
    is_active = db.Column(db.Boolean, default=True)
    is_available_online = db.Column(db.Boolean, default=True)
    requires_approval = db.Column(db.Boolean, default=True)
    
    # Processing Information
    processing_days = db.Column(db.Integer, default=3)  # Expected processing days
    requirements = db.Column(db.Text)  # JSON string of requirements
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def formatted_fee(self):
        """Format fee with currency"""
        return f"₱{float(self.fee):,.2f}" if self.fee else "₱0.00"
    
    @classmethod
    def get_default_types(cls):
        """Get default certificate types for initial setup"""
        return [
            {
                'name': 'Barangay Clearance',
                'code': 'barangay_clearance',
                'description': 'Standard clearance certificate for various purposes',
                'fee': 50.00,
                'processing_days': 3,
                'requirements': '["Valid ID", "Proof of Residency"]'
            },
            {
                'name': 'Certificate of Residency',
                'code': 'certificate_of_residency',
                'description': 'Certificate proving residency in the barangay',
                'fee': 30.00,
                'processing_days': 2,
                'requirements': '["Valid ID", "Proof of Address"]'
            },
            {
                'name': 'Certificate of Indigency',
                'code': 'certificate_of_indigency',
                'description': 'Certificate for indigent residents',
                'fee': 25.00,
                'processing_days': 5,
                'requirements': '["Valid ID", "Proof of Income", "Social Case Study"]'
            },
            {
                'name': 'Business Permit',
                'code': 'business_permit',
                'description': 'Permit for small business operations',
                'fee': 200.00,
                'processing_days': 7,
                'requirements': '["Business Registration", "Valid ID", "Location Map"]'
            },
            {
                'name': 'Health Certificate',
                'code': 'health_certificate',
                'description': 'Health clearance certificate',
                'fee': 100.00,
                'processing_days': 3,
                'requirements': '["Valid ID", "Medical Certificate"]'
            },
            {
                'name': 'Good Moral Character',
                'code': 'good_moral_character',
                'description': 'Certificate of good moral character',
                'fee': 75.00,
                'processing_days': 5,
                'requirements': '["Valid ID", "Character References"]'
            }
        ]
    
    def to_dict(self):
        """Convert certificate type to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'fee': float(self.fee) if self.fee else 0.0,
            'formatted_fee': self.formatted_fee,
            'is_active': self.is_active,
            'is_available_online': self.is_available_online,
            'requires_approval': self.requires_approval,
            'processing_days': self.processing_days,
            'requirements': self.requirements,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<CertificateType {self.name} - ₱{self.formatted_fee}>'

class Official(db.Model):
    __tablename__ = 'officials'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    committee = db.Column(db.String(100))  # Committee assignment
    profile_picture = db.Column(db.String(255), default='no-picture.jpg')  # Profile picture filename
    
    # Contact Information
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Term Information
    term_start = db.Column(db.Date)
    term_end = db.Column(db.Date)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Official {self.name} - {self.position}>'

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Details
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(250))  # URL-friendly version of title
    excerpt = db.Column(db.Text)  # Short summary/description
    
    # Categorization
    category = db.Column(db.String(50), default='general')  # events, notices, emergency, health, services, general
    tags = db.Column(db.Text)  # Comma-separated tags for better organization
    
    # Status Management
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, published, archived, expired
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_featured = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)  # Pin to top
    
    # Publishing & Scheduling
    publish_date = db.Column(db.DateTime)  # When to publish (for scheduling)
    expiry_date = db.Column(db.DateTime)  # When announcement expires
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)  # Actual publish timestamp
    
    # Engagement & Analytics
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    
    # Notification Settings
    send_sms = db.Column(db.Boolean, default=False)
    send_email = db.Column(db.Boolean, default=True)
    post_on_website = db.Column(db.Boolean, default=True)
    notify_residents = db.Column(db.Boolean, default=False)
    
    # Media & Attachments
    featured_image = db.Column(db.String(255))  # Path to featured image
    attachment_path = db.Column(db.String(255))  # Path to attached file
    attachment_name = db.Column(db.String(255))  # Original filename
    attachment_size = db.Column(db.Integer)  # File size in bytes
    
    # Event-specific fields (if announcement is for an event)
    event_date = db.Column(db.DateTime)
    event_time = db.Column(db.Time)
    event_location = db.Column(db.String(200))
    event_organizer = db.Column(db.String(100))
    event_contact = db.Column(db.String(50))
    registration_required = db.Column(db.Boolean, default=False)
    registration_deadline = db.Column(db.DateTime)
    max_participants = db.Column(db.Integer)
    
    # User Management
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', foreign_keys=[created_by], backref='created_announcements')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_announcements')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_announcements')
    
    @property
    def announcement_number(self):
        """Generate announcement number: ANN-YYYY-XXX"""
        if self.id:
            year = self.created_at.year if self.created_at else datetime.utcnow().year
            return f"ANN-{year}-{str(self.id).zfill(3)}"
        return None
    
    @property
    def formatted_category(self):
        """Return formatted category name"""
        category_map = {
            'events': 'Community Events',
            'notices': 'Public Notices',
            'emergency': 'Emergency Alerts',
            'health': 'Health & Safety',
            'services': 'Public Services',
            'government': 'Government Updates',
            'general': 'General Announcements'
        }
        return category_map.get(self.category, self.category.title())
    
    @property
    def formatted_status(self):
        """Return formatted status name"""
        status_map = {
            'draft': 'Draft',
            'scheduled': 'Scheduled',
            'published': 'Published',
            'archived': 'Archived',
            'expired': 'Expired'
        }
        return status_map.get(self.status, self.status.title())
    
    @property
    def is_active(self):
        """Check if announcement is currently active"""
        now = datetime.utcnow()
        if not self.is_published or self.status != 'published':
            return False
        if self.expiry_date and now > self.expiry_date:
            return False
        return True
    
    @property
    def is_scheduled(self):
        """Check if announcement is scheduled for future publishing"""
        return self.status == 'scheduled' and self.publish_date and self.publish_date > datetime.utcnow()
    
    @property
    def is_expired(self):
        """Check if announcement has expired"""
        return self.expiry_date and datetime.utcnow() > self.expiry_date
    
    @property
    def days_until_expiry(self):
        """Calculate days until expiry"""
        if self.expiry_date:
            delta = self.expiry_date - datetime.utcnow()
            return delta.days if delta.days > 0 else 0
        return None
    
    @property
    def formatted_publish_date(self):
        """Format publish date for display"""
        if self.published_at:
            return self.published_at.strftime('%B %d, %Y at %I:%M %p')
        return None
    
    @property
    def formatted_event_date(self):
        """Format event date for display"""
        if self.event_date:
            return self.event_date.strftime('%B %d, %Y')
        return None
    
    def get_tags_list(self):
        """Get tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def set_tags_from_list(self, tags_list):
        """Set tags from a list"""
        if tags_list:
            self.tags = ', '.join([tag.strip() for tag in tags_list if tag.strip()])
        else:
            self.tags = None
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

class BlotterRecord(db.Model):
    __tablename__ = 'blotter_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Case Information
    case_number = db.Column(db.String(50), unique=True, nullable=False)
    complainant_name = db.Column(db.String(100), nullable=False)
    complainant_address = db.Column(db.String(200))
    complainant_contact = db.Column(db.String(20))
    respondent_name = db.Column(db.String(100), nullable=False)
    respondent_address = db.Column(db.String(200))
    respondent_contact = db.Column(db.String(20))
    
    # Incident Details
    incident_date = db.Column(db.DateTime, nullable=False)
    incident_time = db.Column(db.Time)
    incident_place = db.Column(db.String(200))
    incident_type = db.Column(db.String(50))  # noise_complaint, theft, domestic_dispute, public_disturbance, vandalism, others
    incident_description = db.Column(db.Text)
    
    # Status and Priority
    status = db.Column(db.String(30), default='active')  # active, under_investigation, mediation_scheduled, referred_to_police, resolved, closed, dismissed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, emergency
    
    # Processing Information
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_by = db.Column(db.String(100))  # Name of the person who reported
    reporter_type = db.Column(db.String(50))  # resident, barangay_tanod, family_member, neighbor, etc.
    
    # Resolution Details
    resolution_date = db.Column(db.DateTime)
    resolution_details = db.Column(db.Text)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Additional Information
    witnesses = db.Column(db.Text)  # JSON string of witness information
    evidence = db.Column(db.Text)  # Description of evidence
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recorder = db.relationship('User', foreign_keys=[recorded_by], backref='recorded_blotters')
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref='resolved_blotters')
    
    @property
    def blotter_number(self):
        """Generate a formatted blotter number"""
        return f"BLOT-{self.created_at.year}-{str(self.id).zfill(3)}"
    
    @property
    def is_active(self):
        """Check if the blotter case is still active"""
        return self.status in ['active', 'under_investigation', 'mediation_scheduled']
    
    @property
    def is_resolved(self):
        """Check if the blotter case is resolved"""
        return self.status in ['resolved', 'closed']
    
    @property
    def formatted_incident_type(self):
        """Get formatted incident type for display"""
        type_map = {
            'noise_complaint': 'Noise Complaint',
            'theft': 'Theft/Robbery',
            'domestic_dispute': 'Domestic Dispute',
            'public_disturbance': 'Public Disturbance',
            'vandalism': 'Vandalism',
            'others': 'Others'
        }
        return type_map.get(self.incident_type, self.incident_type.replace('_', ' ').title())
    
    @property
    def formatted_status(self):
        """Get formatted status for display"""
        status_map = {
            'active': 'Active',
            'under_investigation': 'Under Investigation',
            'mediation_scheduled': 'Mediation Scheduled',
            'referred_to_police': 'Referred to Police',
            'resolved': 'Resolved',
            'closed': 'Closed',
            'dismissed': 'Dismissed'
        }
        return status_map.get(self.status, self.status.replace('_', ' ').title())
    
    def __repr__(self):
        return f'<BlotterRecord {self.case_number}>'

class SystemActivity(db.Model):
    """Track system activities for dashboard analytics"""
    __tablename__ = 'system_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Activity Information
    activity_type = db.Column(db.String(50), nullable=False)  # login, certificate_request, resident_approval, etc.
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_id = db.Column(db.Integer)  # ID of the affected entity (resident, certificate, etc.)
    target_type = db.Column(db.String(50))  # Type of affected entity
    
    # Metadata
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activities')
    
    def __repr__(self):
        return f'<SystemActivity {self.activity_type} by {self.user_id}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Payment Identification
    payment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    reference_number = db.Column(db.String(100), unique=True, index=True)
    transaction_id = db.Column(db.String(100), index=True)
    
    # Resident Information
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'), nullable=False)
    payer_name = db.Column(db.String(200), nullable=False)
    payer_email = db.Column(db.String(120))
    payer_phone = db.Column(db.String(20))
    
    # Service Information
    service_type = db.Column(db.String(100), nullable=False)  # barangay_clearance, residency_certificate, etc.
    service_description = db.Column(db.Text)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificates.id'), nullable=True)
    
    # Payment Details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='PHP')
    payment_method = db.Column(db.String(50), nullable=False)  # cash, gcash, bank_transfer, online
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid, failed, cancelled, refunded
    
    # Transaction Information
    payment_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    payment_gateway = db.Column(db.String(50))  # gcash, paymaya, instapay, etc.
    gateway_transaction_id = db.Column(db.String(100))
    gateway_response = db.Column(db.Text)  # JSON response from payment gateway
    
    # Receipt and Documentation
    receipt_number = db.Column(db.String(50), unique=True, index=True)
    receipt_issued = db.Column(db.Boolean, default=False)
    receipt_issued_at = db.Column(db.DateTime)
    receipt_issued_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Processing Information
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    processed_at = db.Column(db.DateTime)
    verification_status = db.Column(db.String(20), default='unverified')  # unverified, verified, disputed
    verification_notes = db.Column(db.Text)
    
    # Financial Information
    base_fee = db.Column(db.Numeric(10, 2))
    additional_fees = db.Column(db.Numeric(10, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    discount_reason = db.Column(db.String(200))
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    
    # Refund Information
    refund_amount = db.Column(db.Numeric(10, 2), default=0)
    refund_reason = db.Column(db.String(500))
    refund_date = db.Column(db.DateTime)
    refunded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Administrative Information
    payment_category = db.Column(db.String(50), default='service_fee')  # service_fee, permit_fee, penalty, other
    priority = db.Column(db.String(20), default='normal')  # urgent, high, normal, low
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_period = db.Column(db.String(20))  # monthly, quarterly, annual
    
    # Notification and Communication
    notification_sent = db.Column(db.Boolean, default=False)
    notification_sent_at = db.Column(db.DateTime)
    reminder_count = db.Column(db.Integer, default=0)
    last_reminder_sent = db.Column(db.DateTime)
    
    # Payment List Specific Fields
    is_certificate_payment = db.Column(db.Boolean, default=False)  # Track if this is from a certificate
    moved_to_payment_list = db.Column(db.Boolean, default=False)  # Track if moved to payment list
    moved_to_payment_list_date = db.Column(db.DateTime)  # When moved to payment list
    
    # Audit and Tracking
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)  # Only visible to admin
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resident = db.relationship('Resident', backref='payments')
    certificate = db.relationship('Certificate', backref='payment_records')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_payments')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_payments')
    processor = db.relationship('User', foreign_keys=[processed_by], backref='processed_payments')
    receipt_issuer = db.relationship('User', foreign_keys=[receipt_issued_by], backref='issued_receipts')
    refunder = db.relationship('User', foreign_keys=[refunded_by], backref='processed_refunds')
    
    def __init__(self, **kwargs):
        super(Payment, self).__init__(**kwargs)
        if not self.payment_number:
            self.payment_number = self.generate_payment_number()
        if not self.receipt_number and self.payment_status == 'paid':
            self.receipt_number = self.generate_receipt_number()
    
    def generate_payment_number(self):
        """Generate unique payment number"""
        from datetime import datetime
        year = datetime.now().year
        # Get the count of payments this year
        count = Payment.query.filter(
            Payment.payment_number.like(f'PAY-{year}-%')
        ).count() + 1
        return f'PAY-{year}-{count:06d}'
    
    def generate_receipt_number(self):
        """Generate unique receipt number"""
        from datetime import datetime
        year = datetime.now().year
        month = datetime.now().month
        # Get the count of receipts this month
        count = Payment.query.filter(
            Payment.receipt_number.like(f'RCP-{year}{month:02d}-%')
        ).count() + 1
        return f'RCP-{year}{month:02d}-{count:06d}'
    
    @property
    def total_amount(self):
        """Calculate total amount including fees and taxes, minus discounts"""
        total = float(self.amount or 0)
        total += float(self.additional_fees or 0)
        total += float(self.tax_amount or 0)
        total -= float(self.discount_amount or 0)
        return max(0, total)
    
    @property
    def is_paid(self):
        """Check if payment is completed"""
        return self.payment_status == 'paid'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.payment_status == 'pending'
    
    @property
    def is_overdue(self):
        """Check if payment is overdue"""
        if not self.due_date or self.is_paid:
            return False
        return datetime.utcnow() > self.due_date
    
    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if not self.is_overdue:
            return 0
        return (datetime.utcnow() - self.due_date).days
    
    @property
    def formatted_amount(self):
        """Format amount with currency"""
        return f"₱{self.total_amount:,.2f}"
    
    @property
    def status_badge_class(self):
        """Get CSS class for status badge"""
        status_classes = {
            'paid': 'bg-green-100 text-green-800',
            'pending': 'bg-yellow-100 text-yellow-800',
            'failed': 'bg-red-100 text-red-800',
            'cancelled': 'bg-gray-100 text-gray-800',
            'refunded': 'bg-purple-100 text-purple-800',
            'overdue': 'bg-red-100 text-red-800'
        }
        if self.is_overdue:
            return status_classes.get('overdue', 'bg-gray-100 text-gray-800')
        return status_classes.get(self.payment_status, 'bg-gray-100 text-gray-800')
    
    @property
    def method_badge_class(self):
        """Get CSS class for payment method badge"""
        method_classes = {
            'cash': 'bg-green-100 text-green-800',
            'gcash': 'bg-blue-100 text-blue-800',
            'bank_transfer': 'bg-purple-100 text-purple-800',
            'online': 'bg-indigo-100 text-indigo-800',
            'card': 'bg-gray-100 text-gray-800'
        }
        return method_classes.get(self.payment_method, 'bg-gray-100 text-gray-800')
    
    def mark_as_paid(self, processed_by_id=None):
        """Mark payment as paid"""
        self.payment_status = 'paid'
        self.payment_date = datetime.utcnow()
        self.processed_by = processed_by_id
        self.processed_at = datetime.utcnow()
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
    
    def process_refund(self, amount, reason, processed_by_id):
        """Process refund for payment"""
        if amount > self.total_amount:
            raise ValueError("Refund amount cannot exceed payment amount")
        
        self.refund_amount = amount
        self.refund_reason = reason
        self.refund_date = datetime.utcnow()
        self.refunded_by = processed_by_id
        
        if amount == self.total_amount:
            self.payment_status = 'refunded'
    
    def move_to_payment_list(self):
        """Move payment to payment list"""
        if self.is_certificate_payment and not self.moved_to_payment_list:
            self.moved_to_payment_list = True
            self.moved_to_payment_list_date = datetime.utcnow()
            return True
        return False
    
    @property
    def is_ready_for_payment_list(self):
        """Check if payment is ready to be shown in payment list"""
        return (self.is_certificate_payment and 
                self.moved_to_payment_list and 
                self.payment_status in ['pending', 'paid'])
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'id': self.id,
            'payment_number': self.payment_number,
            'reference_number': self.reference_number,
            'resident_name': self.payer_name,
            'resident_email': self.payer_email,
            'service_type': self.service_type,
            'service_description': self.service_description,
            'amount': float(self.amount),
            'total_amount': self.total_amount,
            'formatted_amount': self.formatted_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'receipt_number': self.receipt_number,
            'is_paid': self.is_paid,
            'is_pending': self.is_pending,
            'is_overdue': self.is_overdue,
            'days_overdue': self.days_overdue,
            'status_badge_class': self.status_badge_class,
            'method_badge_class': self.method_badge_class,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Payment {self.payment_number} - {self.payer_name} - ₱{self.total_amount}>'


class SystemSettings(db.Model):
    """System configuration and general settings"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # System Configuration
    system_name = db.Column(db.String(100), nullable=False, default='iSerBisyo')
    system_version = db.Column(db.String(20), default='1.0.0')
    system_description = db.Column(db.Text)
    
    # Localization
    timezone = db.Column(db.String(50), default='Asia/Manila')
    language = db.Column(db.String(10), default='en')
    date_format = db.Column(db.String(20), default='YYYY-MM-DD')
    currency = db.Column(db.String(10), default='PHP')
    
    # System Behavior
    maintenance_mode = db.Column(db.Boolean, default=False)
    registration_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    
    # File Upload Settings
    max_file_size_mb = db.Column(db.Integer, default=16)  # MB
    allowed_file_types = db.Column(db.Text, default='png,jpg,jpeg,pdf,doc,docx')
    
    # Security Settings
    session_timeout_minutes = db.Column(db.Integer, default=60)
    password_min_length = db.Column(db.Integer, default=8)
    password_expiry_days = db.Column(db.Integer, default=90)
    failed_login_attempts = db.Column(db.Integer, default=5)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        """Get system settings, create default if none exist"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'system_name': self.system_name,
            'system_version': self.system_version,
            'system_description': self.system_description,
            'timezone': self.timezone,
            'language': self.language,
            'date_format': self.date_format,
            'currency': self.currency,
            'maintenance_mode': self.maintenance_mode,
            'registration_enabled': self.registration_enabled,
            'email_notifications': self.email_notifications,
            'sms_notifications': self.sms_notifications,
            'max_file_size_mb': self.max_file_size_mb,
            'allowed_file_types': self.allowed_file_types.split(',') if self.allowed_file_types else [],
            'session_timeout_minutes': self.session_timeout_minutes,
            'password_min_length': self.password_min_length,
            'password_expiry_days': self.password_expiry_days,
            'failed_login_attempts': self.failed_login_attempts,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<SystemSettings {self.system_name}>'


class BarangayInfo(db.Model):
    """Barangay information and contact details"""
    __tablename__ = 'barangay_info'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    barangay_name = db.Column(db.String(100), nullable=False, default='Sample Barangay')
    municipality = db.Column(db.String(100), nullable=False, default='Sample Municipality')
    province = db.Column(db.String(100), nullable=False, default='Sample Province')
    region = db.Column(db.String(100), default='Sample Region')
    zip_code = db.Column(db.String(10))
    
    # Address Details
    street_address = db.Column(db.String(200))
    barangay_hall_address = db.Column(db.Text)
    
    # Contact Information
    phone_number = db.Column(db.String(20))
    mobile_number = db.Column(db.String(20))
    fax_number = db.Column(db.String(20))
    email_address = db.Column(db.String(120))
    website = db.Column(db.String(200))
    facebook_page = db.Column(db.String(200))
    
    # Official Information
    captain_name = db.Column(db.String(100))
    captain_term_start = db.Column(db.Date)
    captain_term_end = db.Column(db.Date)
    secretary_name = db.Column(db.String(100))
    treasurer_name = db.Column(db.String(100))
    
    # Service Information
    office_hours = db.Column(db.Text)  # JSON string for flexible scheduling
    service_days = db.Column(db.String(50), default='Monday to Friday')
    emergency_hotline = db.Column(db.String(20))
    
    # Geographical Information
    total_population = db.Column(db.Integer)
    total_households = db.Column(db.Integer)
    total_area_hectares = db.Column(db.Numeric(10, 2))
    
    # Logo and Images
    logo_filename = db.Column(db.String(200))
    seal_filename = db.Column(db.String(200))
    
    # Additional Information
    mission_statement = db.Column(db.Text)
    vision_statement = db.Column(db.Text)
    brief_history = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_info(cls):
        """Get barangay info, create default if none exist"""
        info = cls.query.first()
        if not info:
            info = cls()
            db.session.add(info)
            db.session.commit()
        return info
    
    @property
    def full_address(self):
        """Get formatted full address"""
        parts = []
        if self.street_address:
            parts.append(self.street_address)
        if self.barangay_name:
            parts.append(self.barangay_name)
        if self.municipality:
            parts.append(self.municipality)
        if self.province:
            parts.append(self.province)
        if self.zip_code:
            parts.append(self.zip_code)
        return ', '.join(parts)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'barangay_name': self.barangay_name,
            'municipality': self.municipality,
            'province': self.province,
            'region': self.region,
            'zip_code': self.zip_code,
            'street_address': self.street_address,
            'barangay_hall_address': self.barangay_hall_address,
            'phone_number': self.phone_number,
            'mobile_number': self.mobile_number,
            'fax_number': self.fax_number,
            'email_address': self.email_address,
            'website': self.website,
            'facebook_page': self.facebook_page,
            'captain_name': self.captain_name,
            'captain_term_start': self.captain_term_start.isoformat() if self.captain_term_start else None,
            'captain_term_end': self.captain_term_end.isoformat() if self.captain_term_end else None,
            'secretary_name': self.secretary_name,
            'treasurer_name': self.treasurer_name,
            'office_hours': self.office_hours,
            'service_days': self.service_days,
            'emergency_hotline': self.emergency_hotline,
            'total_population': self.total_population,
            'total_households': self.total_households,
            'total_area_hectares': float(self.total_area_hectares) if self.total_area_hectares else None,
            'logo_filename': self.logo_filename,
            'seal_filename': self.seal_filename,
            'mission_statement': self.mission_statement,
            'vision_statement': self.vision_statement,
            'brief_history': self.brief_history,
            'full_address': self.full_address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<BarangayInfo {self.barangay_name}, {self.municipality}>'


class ContactMessage(db.Model):
    """Contact messages from website visitors"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Sender Information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    
    # Message Details
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Status and Processing
    status = db.Column(db.String(20), default='unread')  # unread, read, replied, archived
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    
    # Response Information
    response = db.Column(db.Text)  # Admin response to the message
    responded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    responded_at = db.Column(db.DateTime)
    
    # Metadata
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responder = db.relationship('User', foreign_keys=[responded_by], backref='contact_responses')
    
    @property
    def message_number(self):
        """Generate unique message number"""
        if self.id:
            year = self.created_at.year if self.created_at else datetime.utcnow().year
            return f"MSG-{year}-{str(self.id).zfill(4)}"
        return None
    
    @property
    def is_unread(self):
        """Check if message is unread"""
        return self.status == 'unread'
    
    @property
    def is_replied(self):
        """Check if message has been replied to"""
        return self.status == 'replied'
    
    @property
    def formatted_status(self):
        """Get formatted status for display"""
        status_map = {
            'unread': 'Unread',
            'read': 'Read',
            'replied': 'Replied',
            'archived': 'Archived'
        }
        return status_map.get(self.status, self.status.title())
    
    @property
    def status_badge_class(self):
        """Get CSS class for status badge"""
        status_classes = {
            'unread': 'bg-red-100 text-red-800',
            'read': 'bg-blue-100 text-blue-800',
            'replied': 'bg-green-100 text-green-800',
            'archived': 'bg-gray-100 text-gray-800'
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')
    
    @property
    def priority_badge_class(self):
        """Get CSS class for priority badge"""
        priority_classes = {
            'low': 'bg-gray-100 text-gray-800',
            'normal': 'bg-blue-100 text-blue-800',
            'high': 'bg-yellow-100 text-yellow-800',
            'urgent': 'bg-red-100 text-red-800'
        }
        return priority_classes.get(self.priority, 'bg-gray-100 text-gray-800')
    
    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'unread':
            self.status = 'read'
            self.updated_at = datetime.utcnow()
    
    def mark_as_replied(self, response, user_id):
        """Mark message as replied with response"""
        self.status = 'replied'
        self.response = response
        self.responded_by = user_id
        self.responded_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def archive(self):
        """Archive the message"""
        self.status = 'archived'
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'message_number': self.message_number,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'formatted_status': self.formatted_status,
            'priority': self.priority,
            'response': self.response,
            'responded_by': self.responded_by,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'ip_address': self.ip_address,
            'is_unread': self.is_unread,
            'is_replied': self.is_replied,
            'status_badge_class': self.status_badge_class,
            'priority_badge_class': self.priority_badge_class,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ContactMessage {self.message_number} from {self.name}>'


class PurokInfo(db.Model):
    __tablename__ = 'purok_info'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.Enum('Purok', 'Sitio', name='purok_type'), default='Purok')
    description = db.Column(db.Text)
    leader_name = db.Column(db.String(100))
    leader_contact = db.Column(db.String(20))
    leader_address = db.Column(db.String(200))
    boundaries = db.Column(db.Text)
    area_hectares = db.Column(db.Numeric(10, 4))
    population_count = db.Column(db.Integer, default=0)
    household_count = db.Column(db.Integer, default=0)
    barangay_id = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    coordinates_lat = db.Column(db.Numeric(10, 8))
    coordinates_lng = db.Column(db.Numeric(11, 8))
    landmark = db.Column(db.String(200))
    zip_code = db.Column(db.String(10))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_puroks')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='updated_puroks')
    
    @property
    def resident_count(self):
        """Alias for population_count for backward compatibility"""
        return self.population_count
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'leader_name': self.leader_name,
            'leader_contact': self.leader_contact,
            'leader_address': self.leader_address,
            'boundaries': self.boundaries,
            'area_hectares': float(self.area_hectares) if self.area_hectares else None,
            'population_count': self.population_count,
            'household_count': self.household_count,
            'resident_count': self.resident_count,
            'barangay_id': self.barangay_id,
            'is_active': self.is_active,
            'coordinates_lat': float(self.coordinates_lat) if self.coordinates_lat else None,
            'coordinates_lng': float(self.coordinates_lng) if self.coordinates_lng else None,
            'landmark': self.landmark,
            'zip_code': self.zip_code,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PurokInfo {self.name} ({self.type})>'
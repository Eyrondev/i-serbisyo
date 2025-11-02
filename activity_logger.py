"""
Activity logging utilities for the iSerbisyo application
"""

from flask import session, request
from models import db, SystemActivity
from datetime import datetime

def log_activity(activity_type, description, target_id=None, target_type=None, user_id=None):
    """
    Log a system activity
    
    Args:
        activity_type (str): Type of activity (e.g., 'resident_approval', 'login', etc.)
        description (str): Human-readable description of the activity
        target_id (int, optional): ID of the affected entity
        target_type (str, optional): Type of the affected entity
        user_id (int, optional): ID of the user who performed the action
    """
    try:
        # Get user ID from session if not provided
        if user_id is None:
            user_data = session.get('user', {})
            user_id = user_data.get('id')
        
        # Get client IP address
        ip_address = None
        if request:
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip_address and ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()
        
        # Get user agent
        user_agent = None
        if request:
            user_agent = request.headers.get('User-Agent', '')[:500]  # Limit length
        
        # Create activity record
        activity = SystemActivity(
            activity_type=activity_type,
            description=description,
            user_id=user_id,
            target_id=target_id,
            target_type=target_type,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow()
        )
        
        db.session.add(activity)
        db.session.commit()
        
    except Exception as e:
        # Don't let logging errors break the main functionality
        print(f"Error logging activity: {e}")
        try:
            db.session.rollback()
        except:
            pass

# Predefined activity types for consistency
class ActivityTypes:
    # Authentication
    LOGIN = 'login'
    LOGOUT = 'logout'
    FAILED_LOGIN = 'failed_login'
    
    # Resident Management
    RESIDENT_REGISTRATION = 'resident_registration'
    RESIDENT_APPROVAL = 'resident_approval'
    RESIDENT_REJECTION = 'resident_rejection'
    RESIDENT_UPDATE = 'resident_update'
    RESIDENT_DELETE = 'resident_delete'
    
    # Certificate Management
    CERTIFICATE_REQUEST = 'certificate_request'
    CERTIFICATE_APPROVAL = 'certificate_approval'
    CERTIFICATE_REJECTION = 'certificate_rejection'
    CERTIFICATE_CLAIMED = 'certificate_claimed'
    CERTIFICATE_PAYMENT = 'certificate_payment'
    
    # Document Management
    DOCUMENT_UPLOAD = 'document_upload'
    DOCUMENT_DELETE = 'document_delete'
    DOCUMENT_DOWNLOAD = 'document_download'
    
    # Announcements
    ANNOUNCEMENT_CREATE = 'announcement_create'
    ANNOUNCEMENT_UPDATE = 'announcement_update'
    ANNOUNCEMENT_DELETE = 'announcement_delete'
    ANNOUNCEMENT_PUBLISH = 'announcement_publish'
    
    # Officials Management
    OFFICIAL_CREATE = 'official_create'
    OFFICIAL_UPDATE = 'official_update'
    OFFICIAL_DELETE = 'official_delete'
    
    # Blotter Records
    BLOTTER_CREATE = 'blotter_create'
    BLOTTER_UPDATE = 'blotter_update'
    BLOTTER_RESOLVE = 'blotter_resolve'
    
    # System Activities
    SYSTEM_BACKUP = 'system_backup'
    SYSTEM_RESTORE = 'system_restore'
    SETTINGS_UPDATE = 'settings_update'
    
    # Payment Management
    PAYMENT_RECEIVED = 'payment_received'
    PAYMENT_REFUND = 'payment_refund'

def log_login(user_name, user_id, success=True):
    """Log user login activity"""
    if success:
        log_activity(
            ActivityTypes.LOGIN,
            f"User {user_name} logged in successfully",
            user_id=user_id,
            target_id=user_id,
            target_type='user'
        )
    else:
        log_activity(
            ActivityTypes.FAILED_LOGIN,
            f"Failed login attempt for user {user_name}",
            target_type='user'
        )

def log_logout(user_name, user_id):
    """Log user logout activity"""
    log_activity(
        ActivityTypes.LOGOUT,
        f"User {user_name} logged out",
        user_id=user_id,
        target_id=user_id,
        target_type='user'
    )

def log_resident_action(action_type, resident_name, resident_id, user_id=None):
    """Log resident-related activities"""
    action_descriptions = {
        ActivityTypes.RESIDENT_APPROVAL: f"Resident {resident_name} approved",
        ActivityTypes.RESIDENT_REJECTION: f"Resident {resident_name} rejected",
        ActivityTypes.RESIDENT_REGISTRATION: f"New resident {resident_name} registered",
        ActivityTypes.RESIDENT_UPDATE: f"Resident {resident_name} information updated",
        ActivityTypes.RESIDENT_DELETE: f"Resident {resident_name} deleted"
    }
    
    description = action_descriptions.get(action_type, f"Resident action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=resident_id,
        target_type='resident'
    )

def log_certificate_action(action_type, certificate_type, resident_name, certificate_id, user_id=None):
    """Log certificate-related activities"""
    action_descriptions = {
        ActivityTypes.CERTIFICATE_REQUEST: f"Certificate request: {certificate_type} for {resident_name}",
        ActivityTypes.CERTIFICATE_APPROVAL: f"Certificate approved: {certificate_type} for {resident_name}",
        ActivityTypes.CERTIFICATE_REJECTION: f"Certificate rejected: {certificate_type} for {resident_name}",
        ActivityTypes.CERTIFICATE_CLAIMED: f"Certificate claimed: {certificate_type} by {resident_name}",
        ActivityTypes.CERTIFICATE_PAYMENT: f"Payment received: {certificate_type} for {resident_name}"
    }
    
    description = action_descriptions.get(action_type, f"Certificate action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=certificate_id,
        target_type='certificate'
    )

def log_announcement_action(action_type, title, announcement_id, user_id=None):
    """Log announcement-related activities"""
    action_descriptions = {
        ActivityTypes.ANNOUNCEMENT_CREATE: f"Announcement created: {title}",
        ActivityTypes.ANNOUNCEMENT_UPDATE: f"Announcement updated: {title}",
        ActivityTypes.ANNOUNCEMENT_DELETE: f"Announcement deleted: {title}",
        ActivityTypes.ANNOUNCEMENT_PUBLISH: f"Announcement published: {title}"
    }
    
    description = action_descriptions.get(action_type, f"Announcement action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=announcement_id,
        target_type='announcement'
    )

def log_official_action(action_type, official_name, official_id, user_id=None):
    """Log official-related activities"""
    action_descriptions = {
        ActivityTypes.OFFICIAL_CREATE: f"Official added: {official_name}",
        ActivityTypes.OFFICIAL_UPDATE: f"Official updated: {official_name}",
        ActivityTypes.OFFICIAL_DELETE: f"Official removed: {official_name}"
    }
    
    description = action_descriptions.get(action_type, f"Official action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=official_id,
        target_type='official'
    )

def log_blotter_action(action_type, case_number, blotter_id, user_id=None):
    """Log blotter-related activities"""
    action_descriptions = {
        ActivityTypes.BLOTTER_CREATE: f"Blotter record created: {case_number}",
        ActivityTypes.BLOTTER_UPDATE: f"Blotter record updated: {case_number}",
        ActivityTypes.BLOTTER_RESOLVE: f"Blotter record resolved: {case_number}"
    }
    
    description = action_descriptions.get(action_type, f"Blotter action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=blotter_id,
        target_type='blotter'
    )

def log_payment_action(action_type, payment_number, amount, resident_name, payment_id, user_id=None):
    """Log payment-related activities"""
    action_descriptions = {
        ActivityTypes.PAYMENT_RECEIVED: f"Payment received: {payment_number} - ₱{amount:.2f} from {resident_name}",
        ActivityTypes.PAYMENT_REFUND: f"Payment refunded: {payment_number} - ₱{amount:.2f} to {resident_name}"
    }
    
    description = action_descriptions.get(action_type, f"Payment action: {action_type}")
    log_activity(
        action_type,
        description,
        user_id=user_id,
        target_id=payment_id,
        target_type='payment'
    )
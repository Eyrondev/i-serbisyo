"""
Utility functions and decorators for i-Serbisyo application
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from models import User

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def get_current_user():
    """Get current authenticated user"""
    if is_authenticated():
        return User.query.get(session['user_id'])
    return None

def require_auth(role=None, roles=None):
    """
    Decorator to require authentication and optionally specific role(s)
    
    Args:
        role (str): Single role required (e.g., 'admin')
        roles (list): Multiple roles allowed (e.g., ['admin', 'clerk'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'message': 'Authentication required'}), 401
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('auth.login'))
            
            # Check role requirements
            if role or roles:
                user = get_current_user()
                if not user:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': 'User not found'}), 401
                    flash('User session invalid.', 'error')
                    return redirect(url_for('auth.login'))
                
                # Check single role
                if role and user.role != role:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
                    flash('Access denied. Insufficient permissions.', 'error')
                    return redirect(url_for('public.index'))
                
                # Check multiple roles
                if roles and user.role not in roles:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403
                    flash('Access denied. Insufficient permissions.', 'error')
                    return redirect(url_for('public.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator requiring admin role"""
    return require_auth(role='admin')(f)

def clerk_required(f):
    """Decorator requiring clerk or admin role"""
    return require_auth(roles=['admin', 'clerk'])(f)

def resident_required(f):
    """Decorator requiring resident role"""
    return require_auth(role='resident')(f)

def validate_form_data(form_data, required_fields):
    """
    Validate form data for required fields
    
    Args:
        form_data (dict): Form data to validate
        required_fields (list): List of required field names
    
    Returns:
        dict: Dictionary of validation errors
    """
    errors = {}
    
    for field in required_fields:
        if not form_data.get(field) or form_data.get(field).strip() == '':
            # Convert camelCase to readable names
            field_name = field.replace('_', ' ').title()
            if field == 'firstName':
                field_name = 'First Name'
            elif field == 'lastName':
                field_name = 'Last Name'
            elif field == 'birthDate':
                field_name = 'Birth Date'
            elif field == 'birthPlace':
                field_name = 'Birth Place'
            elif field == 'civilStatus':
                field_name = 'Civil Status'
            elif field == 'houseNumber':
                field_name = 'House Number'
            elif field == 'confirmPassword':
                field_name = 'Confirm Password'
            
            errors[field] = f'{field_name} is required'
    
    return errors

def validate_email(email):
    """Validate email format"""
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return False
    return True

def validate_password(password, min_length=8):
    """Validate password strength"""
    errors = []
    
    if len(password) < min_length:
        errors.append(f'Password must be at least {min_length} characters long')
    
    # Add more password validation rules as needed
    # if not any(c.isupper() for c in password):
    #     errors.append('Password must contain at least one uppercase letter')
    
    return errors

def success_response(message, data=None, redirect_url=None):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message
    }
    if data:
        response['data'] = data
    if redirect_url:
        response['redirect_url'] = redirect_url
    
    return response

def error_response(message, errors=None, status_code=400):
    """Standard error response format"""
    response = {
        'success': False,
        'message': message
    }
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code
from flask import render_template, request, redirect, url_for, session, flash, jsonify, current_app
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from . import auth_bp
from models import User, Resident, db
from utils import success_response, error_response
from activity_logger import log_login, log_logout
import random
import string

# Add CORS headers for AJAX requests
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

def generate_otp():
    """Generate a 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user_email, otp_code, user_name):
    """Send OTP code via email"""
    try:
        from flask_mail import Message, Mail
        from flask import current_app
        
        mail = Mail(current_app)
        
        msg = Message(
            'i-Serbisyo Login Verification Code',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email]
        )
        
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">i-Serbisyo Login Verification</h2>
            <p>Hello {user_name},</p>
            <p>Your verification code for login is:</p>
            <div style="background-color: #f3f4f6; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px;">
                <h1 style="color: #2563eb; font-size: 36px; letter-spacing: 8px; margin: 0;">{otp_code}</h1>
            </div>
            <p>This code will expire in 5 minutes.</p>
            <p>If you didn't attempt to log in, please ignore this email and contact your barangay administrator.</p>
            <hr style="border: 1px solid #e5e7eb; margin: 20px 0;">
            <p style="color: #6b7280; font-size: 12px;">This is an automated message from i-Serbisyo Barangay Management System.</p>
        </div>
        """
        
        mail.send(msg)
        print(f"OTP email sent to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False

@auth_bp.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        return add_cors_headers(response)
    if request.method == 'POST':
        # Always return JSON for POST requests to support AJAX
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            
            # Debug logging
            print(f"AUTH LOGIN ATTEMPT - Email: {email}")
            print(f"Headers: {dict(request.headers)}")
            
            # Basic validation
            if not email or not password:
                print("VALIDATION ERROR - Missing email or password")
                return jsonify({
                    'success': False,
                    'message': 'Email and password are required'
                }), 400
            
            # Find user by email or username
            user = User.query.filter(
                (User.email == email) | (User.username == email)
            ).first()
            
            print(f"USER FOUND: {bool(user)}")
            if user:
                print(f"User details: {user.username} ({user.email}), Active: {user.is_active}")
                password_valid = check_password_hash(user.password, password)
                print(f"Password valid: {password_valid}")
            else:
                print(f"No user found with email/username: {email}")
            
            if not user:
                print("AUTHENTICATION ERROR - User not found")
                # Log failed login attempt
                log_login(email, None, success=False)
                response = jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                })
                return add_cors_headers(response), 401
                
            if not check_password_hash(user.password, password):
                print("AUTHENTICATION ERROR - Invalid password")
                # Log failed login attempt
                log_login(user.name, user.id, success=False)
                response = jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                })
                return add_cors_headers(response), 401
            
            # Check if user account is active
            if not user.is_active:
                message = 'Your account is not active. Please contact administrator.'
                print(f"INACTIVE ACCOUNT - User: {user.username}")
                return jsonify({
                    'success': False,
                    'message': message
                }), 403
            
            # For residents, check their profile status and send OTP
            if user.role == 'resident':
                from models import Resident
                resident_profile = Resident.query.filter_by(user_id=user.id).first()
                
                if not resident_profile:
                    message = 'Your resident profile is not found. Please contact administrator.'
                    print(f"NO RESIDENT PROFILE - User: {user.username}")
                    return jsonify({
                        'success': False,
                        'message': message
                    }), 403
                
                if resident_profile.status == 'pending':
                    message = 'Your resident application is pending approval. Please wait for admin verification.'
                    print(f"PENDING RESIDENT - User: {user.username}, Profile: {resident_profile.status}")
                    return jsonify({
                        'success': False,
                        'message': message,
                        'pending_approval': True
                    }), 403
                
                if resident_profile.status == 'rejected':
                    message = 'Your resident application has been rejected. Please contact administrator.'
                    print(f"REJECTED RESIDENT - User: {user.username}, Profile: {resident_profile.status}")
                    return jsonify({
                        'success': False,
                        'message': message
                    }), 403
                
                # Generate and send OTP for resident login
                otp_code = generate_otp()
                user.otp_code = otp_code
                user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
                user.otp_verified = False
                db.session.commit()
                
                print(f"OTP GENERATED for {user.email}: {otp_code}")
                
                # Send OTP email
                if send_otp_email(user.email, otp_code, user.name):
                    # Store user info in session temporarily for OTP verification
                    session['otp_user_id'] = user.id
                    session.modified = True
                    
                    return jsonify({
                        'success': True,
                        'require_otp': True,
                        'message': f'Verification code sent to {user.email}. Please check your email.',
                        'user_id': user.id
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Failed to send verification code. Please try again or contact administrator.'
                    }), 500
            
            # For admin and clerk - direct login without OTP
            session.permanent = True  # Make session permanent
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['user_name'] = user.name
            session['user'] = {
                'id': user.id,
                'role': user.role,
                'name': user.name,
                'email': user.email
            }
            
            # Force session save
            session.modified = True
            
            print(f"SESSION CREATED - Session ID: {session.get('user_id')}, Data: {dict(session)}")
            
            # Log successful login activity
            log_login(user.name, user.id, success=True)
            
            # Determine redirect URL based on role
            if user.role == 'admin':
                redirect_url = url_for('admin.dashboard')
            elif user.role == 'clerk':
                redirect_url = url_for('clerk.dashboard')
            else:
                redirect_url = url_for('public.index')
            
            # Always return JSON for POST requests
            print(f"LOGIN SUCCESS - Redirecting to: {redirect_url}")
            response = jsonify({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': redirect_url,
                'user': {
                    'id': user.id,
                    'role': user.role,
                    'name': user.name,
                    'email': user.email
                }
            })
            response = add_cors_headers(response)
            
            # Ensure session cookie is sent
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            
            return response
            
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            print(f"LOGIN EXCEPTION - Error: {error_message}")
            return jsonify({
                'success': False,
                'message': error_message
            }), 500
    
    return render_template('public/login.html')

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP code for resident login"""
    try:
        otp_code = request.form.get('otp_code', '').strip()
        user_id = session.get('otp_user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Session expired. Please login again.'
            }), 400
        
        if not otp_code:
            return jsonify({
                'success': False,
                'message': 'Please enter the verification code.'
            }), 400
        
        # Find user
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found. Please login again.'
            }), 404
        
        # Check if OTP is expired
        if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
            return jsonify({
                'success': False,
                'message': 'Verification code has expired. Please login again.'
            }), 400
        
        # Verify OTP code
        if user.otp_code != otp_code:
            return jsonify({
                'success': False,
                'message': 'Invalid verification code. Please try again.'
            }), 400
        
        # OTP verified successfully - create full session
        user.otp_verified = True
        user.otp_code = None
        user.otp_expiry = None
        db.session.commit()
        
        # Clear temporary OTP session
        session.pop('otp_user_id', None)
        
        # Create full login session
        session.permanent = True
        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_name'] = user.name
        session['user'] = {
            'id': user.id,
            'role': user.role,
            'name': user.name,
            'email': user.email
        }
        session.modified = True
        
        print(f"OTP VERIFIED - User: {user.email}, Session created")
        
        # Log successful login
        log_login(user.name, user.id, success=True)
        
        # Redirect to resident dashboard
        redirect_url = url_for('resident.dashboard')
        
        return jsonify({
            'success': True,
            'message': 'Verification successful! Redirecting...',
            'redirect_url': redirect_url
        })
        
    except Exception as e:
        print(f"OTP VERIFICATION ERROR: {e}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP code to user's email"""
    try:
        user_id = session.get('otp_user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Session expired. Please login again.'
            }), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found. Please login again.'
            }), 404
        
        # Generate new OTP
        otp_code = generate_otp()
        user.otp_code = otp_code
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()
        
        print(f"OTP RESENT for {user.email}: {otp_code}")
        
        # Send OTP email
        if send_otp_email(user.email, otp_code, user.name):
            return jsonify({
                'success': True,
                'message': 'New verification code sent to your email.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send verification code. Please try again.'
            }), 500
            
    except Exception as e:
        print(f"OTP RESEND ERROR: {e}")
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

@auth_bp.route('/logout')
def logout():
    # Log logout activity before clearing session
    user_data = session.get('user', {})
    if user_data.get('id') and user_data.get('name'):
        log_logout(user_data.get('name'), user_data.get('id'))
    
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('public.index'))

@auth_bp.route('/debug-session')
def debug_session():
    """Debug route to check session status"""
    return jsonify({
        'session_data': dict(session),
        'user_id': session.get('user_id'),
        'user_role': session.get('user_role'),
        'is_authenticated': 'user_id' in session,
        'cookies': dict(request.cookies),
        'flask_session_info': {
            'permanent': session.permanent,
            'modified': session.modified,
            'secret_key_set': bool(current_app.config.get('SECRET_KEY')),
            'session_cookie_name': current_app.config.get('SESSION_COOKIE_NAME', 'session')
        }
    })

@auth_bp.route('/test-session', methods=['POST'])
def test_session():
    """Test route to verify session functionality"""
    session['test_key'] = 'test_value'
    session['timestamp'] = str(datetime.now())
    session.permanent = True
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': 'Test session created',
        'session_data': dict(session)
    })

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password functionality"""
    if request.method == 'POST':
        try:
            from models import db
            from datetime import datetime, timedelta
            from email_utils import generate_reset_token, send_password_reset_email
            
            email = request.form.get('email', '').strip()
            
            if not email:
                return jsonify({
                    'success': False,
                    'message': 'Email is required'
                }), 400
            
            # Validate email format
            import re
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                return jsonify({
                    'success': False,
                    'message': 'Please enter a valid email address'
                }), 400
            
            # Check if user exists
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Inform user that email is not registered
                return jsonify({
                    'success': False,
                    'message': 'This email address is not registered in our system.'
                }), 404
            
            # Check if user account is active
            if not user.is_active:
                return jsonify({
                    'success': False,
                    'message': 'This account is currently inactive. Please contact the administrator.'
                }), 403
            
            # Generate reset token
            reset_token = generate_reset_token()
            user.reset_token = reset_token
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
            db.session.commit()
            
            # Generate reset link
            reset_link = url_for('auth.reset_password', token=reset_token, _external=True)
            
            # Send email
            email_sent = send_password_reset_email(user.email, reset_link)
            
            if email_sent:
                print(f"PASSWORD RESET EMAIL SENT - Email: {email}, Token: {reset_token}")
                return jsonify({
                    'success': True,
                    'message': 'Password reset instructions have been sent to your email.',
                    'email': email
                })
            else:
                # Email sending failed
                return jsonify({
                    'success': False,
                    'message': 'Failed to send email. Please check your email configuration or try again later.'
                }), 500
            
        except Exception as e:
            print(f"FORGOT PASSWORD ERROR - Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }), 500
    
    return render_template('public/forgot-password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    if request.method == 'POST':
        try:
            from models import db
            from datetime import datetime
            from werkzeug.security import generate_password_hash
            
            # Get form data
            new_password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validate passwords
            if not new_password or not confirm_password:
                return jsonify({
                    'success': False,
                    'message': 'Both password fields are required'
                }), 400
            
            if new_password != confirm_password:
                return jsonify({
                    'success': False,
                    'message': 'Passwords do not match'
                }), 400
            
            if len(new_password) < 8:
                return jsonify({
                    'success': False,
                    'message': 'Password must be at least 8 characters long'
                }), 400
            
            # Find user with this reset token
            user = User.query.filter_by(reset_token=token).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired reset token'
                }), 404
            
            # Check if token has expired
            if user.reset_token_expiry and user.reset_token_expiry < datetime.utcnow():
                return jsonify({
                    'success': False,
                    'message': 'This reset link has expired. Please request a new one.'
                }), 400
            
            # Update password
            user.password = generate_password_hash(new_password)
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            
            print(f"PASSWORD RESET SUCCESS - Email: {user.email}")
            
            return jsonify({
                'success': True,
                'message': 'Password has been reset successfully! You can now login with your new password.'
            })
            
        except Exception as e:
            print(f"RESET PASSWORD ERROR - Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }), 500
    
    # GET request - verify token and show reset form
    try:
        from datetime import datetime
        
        user = User.query.filter_by(reset_token=token).first()
        
        if not user:
            return render_template('public/reset-password.html', 
                                 token=token, 
                                 valid=False, 
                                 message='Invalid reset token')
        
        # Check if token has expired
        if user.reset_token_expiry and user.reset_token_expiry < datetime.utcnow():
            return render_template('public/reset-password.html', 
                                 token=token, 
                                 valid=False, 
                                 message='This reset link has expired')
        
        return render_template('public/reset-password.html', 
                             token=token, 
                             valid=True, 
                             email=user.email)
        
    except Exception as e:
        print(f"RESET PASSWORD PAGE ERROR - Error: {str(e)}")
        return render_template('public/reset-password.html', 
                             token=token, 
                             valid=False, 
                             message='An error occurred')

# Note: Authentication helper functions moved to utils.py for reusability
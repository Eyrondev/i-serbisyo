"""
Email utility functions for i-Serbisyo
Handles sending emails for password reset and notifications
"""
from flask import current_app, render_template_string
from flask_mail import Message
import secrets
from datetime import datetime, timedelta

def generate_reset_token():
    """Generate a secure random token for password reset"""
    return secrets.token_urlsafe(32)

def send_password_reset_email(user_email, reset_link):
    """
    Send password reset email to user
    
    Args:
        user_email (str): User's email address
        reset_link (str): Password reset link URL
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        from app import mail
        
        # Email subject
        subject = "Password Reset Request - i-Serbisyo"
        
        # Email body (HTML)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    line-height: 1.6;
                    color: #1f2937;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 20px;
                }}
                
                .email-wrapper {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                }}
                
                .header {{
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    padding: 48px 40px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                
                .header::before {{
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
                    background-size: 50px 50px;
                    animation: backgroundScroll 20s linear infinite;
                }}
                
                @keyframes backgroundScroll {{
                    0% {{ transform: translate(0, 0); }}
                    100% {{ transform: translate(50px, 50px); }}
                }}
                
                .logo-container {{
                    position: relative;
                    z-index: 1;
                    margin-bottom: 20px;
                }}
                
                .logo-icon {{
                    width: 64px;
                    height: 64px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 32px;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                }}
                
                .header h1 {{
                    position: relative;
                    z-index: 1;
                    color: #ffffff;
                    font-size: 28px;
                    font-weight: 700;
                    margin-bottom: 8px;
                    letter-spacing: -0.5px;
                }}
                
                .header p {{
                    position: relative;
                    z-index: 1;
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 15px;
                    font-weight: 500;
                }}
                
                .content {{
                    padding: 48px 40px;
                    background: #ffffff;
                }}
                
                .greeting {{
                    font-size: 24px;
                    font-weight: 600;
                    color: #111827;
                    margin-bottom: 16px;
                }}
                
                .message {{
                    font-size: 16px;
                    color: #4b5563;
                    margin-bottom: 32px;
                    line-height: 1.7;
                }}
                
                .button-container {{
                    text-align: center;
                    margin: 40px 0;
                }}
                
                .button {{
                    display: inline-block;
                    padding: 16px 40px;
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 600;
                    font-size: 16px;
                    letter-spacing: 0.3px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3), 0 2px 4px -1px rgba(37, 99, 235, 0.2);
                }}
                
                .button:hover {{
                    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4), 0 4px 6px -2px rgba(37, 99, 235, 0.3);
                    transform: translateY(-2px);
                }}
                
                .divider {{
                    text-align: center;
                    margin: 32px 0;
                    position: relative;
                }}
                
                .divider::before {{
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 0;
                    right: 0;
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
                }}
                
                .divider span {{
                    background: #ffffff;
                    padding: 0 16px;
                    color: #9ca3af;
                    font-size: 13px;
                    font-weight: 500;
                    position: relative;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .link-box {{
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 24px 0;
                }}
                
                .link-label {{
                    font-size: 13px;
                    color: #6b7280;
                    font-weight: 500;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                
                .link-text {{
                    word-break: break-all;
                    color: #3b82f6;
                    font-size: 14px;
                    font-family: 'Courier New', monospace;
                }}
                
                .warning-box {{
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    border-left: 4px solid #f59e0b;
                    border-radius: 12px;
                    padding: 24px;
                    margin: 32px 0;
                }}
                
                .warning-box strong {{
                    display: flex;
                    align-items: center;
                    font-size: 15px;
                    color: #92400e;
                    margin-bottom: 12px;
                    font-weight: 600;
                }}
                
                .warning-box ul {{
                    margin: 0;
                    padding-left: 20px;
                    color: #78350f;
                }}
                
                .warning-box li {{
                    margin: 8px 0;
                    font-size: 14px;
                    line-height: 1.6;
                }}
                
                .info-card {{
                    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                    border-radius: 12px;
                    padding: 20px;
                    margin: 24px 0;
                    border: 1px solid #bfdbfe;
                }}
                
                .info-card p {{
                    color: #1e40af;
                    font-size: 14px;
                    margin: 0;
                    line-height: 1.6;
                }}
                
                .signature {{
                    margin-top: 40px;
                    padding-top: 24px;
                    border-top: 1px solid #e5e7eb;
                }}
                
                .signature p {{
                    color: #6b7280;
                    font-size: 15px;
                    margin: 4px 0;
                }}
                
                .signature strong {{
                    color: #111827;
                    font-weight: 600;
                }}
                
                .footer {{
                    background: #f9fafb;
                    padding: 32px 40px;
                    text-align: center;
                    border-top: 1px solid #e5e7eb;
                }}
                
                .footer p {{
                    color: #6b7280;
                    font-size: 13px;
                    margin: 8px 0;
                    line-height: 1.6;
                }}
                
                .social-links {{
                    margin: 20px 0;
                }}
                
                .social-links a {{
                    display: inline-block;
                    width: 36px;
                    height: 36px;
                    background: #e5e7eb;
                    border-radius: 50%;
                    margin: 0 6px;
                    line-height: 36px;
                    color: #6b7280;
                    text-decoration: none;
                    transition: all 0.3s ease;
                }}
                
                .social-links a:hover {{
                    background: #3b82f6;
                    color: #ffffff;
                    transform: translateY(-2px);
                }}
                
                @media only screen and (max-width: 600px) {{
                    body {{
                        padding: 20px 10px;
                    }}
                    
                    .email-wrapper {{
                        border-radius: 12px;
                    }}
                    
                    .header {{
                        padding: 36px 24px;
                    }}
                    
                    .header h1 {{
                        font-size: 24px;
                    }}
                    
                    .content {{
                        padding: 32px 24px;
                    }}
                    
                    .greeting {{
                        font-size: 20px;
                    }}
                    
                    .message {{
                        font-size: 15px;
                    }}
                    
                    .button {{
                        padding: 14px 32px;
                        font-size: 15px;
                    }}
                    
                    .footer {{
                        padding: 24px 20px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <!-- Header -->
                <div class="header">
                    <div class="logo-container">
                        <div class="logo-icon">🔐</div>
                    </div>
                    <h1>Password Reset Request</h1>
                    <p>i-Serbisyo Barangay Management System</p>
                </div>
                
                <!-- Content -->
                <div class="content">
                    <div class="greeting">Hello there! 👋</div>
                    
                    <p class="message">
                        We received a request to reset your password for your i-Serbisyo account. 
                        Don't worry, we've got you covered! Click the button below to create a new secure password.
                    </p>
                    
                    <!-- Reset Button -->
                    <div class="button-container">
                        <a href="{reset_link}" class="button">Reset My Password</a>
                    </div>
                    
                    <!-- Divider -->
                    <div class="divider">
                        <span>Or use this link</span>
                    </div>
                    
                    <!-- Alternative Link -->
                    <div class="link-box">
                        <div class="link-label">Copy and paste this URL:</div>
                        <div class="link-text">{reset_link}</div>
                    </div>
                    
                    <!-- Security Warning -->
                    <div class="warning-box">
                        <strong>⚠️ Important Security Information</strong>
                        <ul>
                            <li>This reset link will <strong>expire in 1 hour</strong> for your security</li>
                            <li>If you didn't request this password reset, you can safely ignore this email</li>
                            <li>Never share this link with anyone - we will never ask for it</li>
                            <li>Make sure you're on the official i-Serbisyo website before entering your new password</li>
                        </ul>
                    </div>
                    
                    <!-- Help Info -->
                    <div class="info-card">
                        <p>
                            <strong>Need help?</strong> If you have any questions or concerns about your account security, 
                            please don't hesitate to contact our support team. We're here to help!
                        </p>
                    </div>
                    
                    <!-- Signature -->
                    <div class="signature">
                        <p>Best regards,</p>
                        <p><strong>The i-Serbisyo Team</strong></p>
                        <p style="color: #9ca3af; font-size: 13px; margin-top: 8px;">
                            Making barangay services accessible to everyone
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <p style="font-weight: 500; color: #111827; margin-bottom: 12px;">i-Serbisyo</p>
                    <p>Barangay Management System</p>
                    <p style="margin-top: 16px;">&copy; 2025 i-Serbisyo. All rights reserved.</p>
                    <p style="font-size: 12px; color: #9ca3af; margin-top: 12px;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        Password Reset Request - i-Serbisyo
        
        Hello!
        
        We received a request to reset your password. Click the link below to create a new password:
        
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        i-Serbisyo Team
        
        ---
        © 2025 i-Serbisyo. All rights reserved.
        This is an automated email. Please do not reply.
        """
        
        # Create message
        msg = Message(
            subject=subject,
            sender=current_app.config.get('MAIL_USERNAME', 'noreply@iserbisyo.com'),
            recipients=[user_email]
        )
        msg.body = text_body
        msg.html = html_body
        
        # Send email
        mail.send(msg)
        
        current_app.logger.info(f"Password reset email sent to {user_email}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email to {user_email}: {str(e)}")
        return False

def send_test_email(to_email):
    """
    Send a test email to verify email configuration
    
    Args:
        to_email (str): Recipient email address
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        from app import mail
        
        msg = Message(
            subject="Test Email - i-Serbisyo",
            sender=current_app.config.get('MAIL_USERNAME', 'noreply@iserbisyo.com'),
            recipients=[to_email]
        )
        msg.body = "This is a test email from i-Serbisyo. If you received this, your email configuration is working correctly!"
        msg.html = "<p>This is a test email from <strong>i-Serbisyo</strong>.</p><p>If you received this, your email configuration is working correctly!</p>"
        
        mail.send(msg)
        
        current_app.logger.info(f"Test email sent to {to_email}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send test email to {to_email}: {str(e)}")
        return False

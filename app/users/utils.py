from flask import url_for, current_app
from flask_mail import Message
from app import mail

def save_picture(form_picture):
    # Function to save profile pictures (implementation not included in the provided snippet)
    pass

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def send_verification_email(user):
    token = user.get_verification_token()
    msg = Message('Account Verification',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To verify your account, visit the following link:
{url_for('users.verify_email', token=token, _external=True)}
If you did not make this request then simply ignore this email.
'''
    mail.send(msg)

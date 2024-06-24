import requests
from flask import url_for, current_app
import logging

def save_picture(form_picture):
    # Function to save profile pictures (implementation not included in the provided snippet)
    pass

def send_reset_email(user):
    token = user.get_reset_token()
    subject = 'Password Reset Request'
    body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    send_email(subject, user.email, body)

def send_verification_email(user):
    token = user.get_verification_token()
    subject = 'Account Verification'
    body = f'''To verify your account, visit the following link:
    {url_for('users.verify_email', token=token, _external=True)}
    If you did not make this request, then simply ignore this email.
    '''
    send_email(subject, user.email, body)

def send_email(subject, to, body):
    logging.debug(f'Sending email to {to} with subject: {subject}')
    logging.debug(f'MAILGUN_DOMAIN: {current_app.config["MAILGUN_DOMAIN"]}')
    logging.debug(f'MAILGUN_API_KEY: {current_app.config["MAILGUN_API_KEY"]}')
    logging.debug(f'MAILGUN_SMTP_LOGIN: {current_app.config["MAILGUN_SMTP_LOGIN"]}')
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{current_app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={"from": f"CyAware <{current_app.config['MAILGUN_SMTP_LOGIN']}>",
              "to": [to],
              "subject": subject,
              "text": body})
    if response.status_code == 200:
        current_app.logger.info(f'Email sent to {to}: {subject}')
    else:
        current_app.logger.error(f'Failed to send email to {to}: {response.text}')
    return response

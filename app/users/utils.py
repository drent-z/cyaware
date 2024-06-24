import requests
from flask import url_for, current_app, render_template
import logging

def save_picture(form_picture):
    # Function to save profile pictures (implementation not included in the provided snippet)
    pass

def send_reset_email(user):
    token = user.get_reset_token()
    subject = 'Password Reset Request'
    send_email(
        subject,
        user.email,
        'emails/reset_password.txt',
        'emails/reset_password.html',
        token=token
    )

def send_verification_email(user):
    token = user.get_verification_token()
    subject = 'Account Verification'
    send_email(
        subject,
        user.email,
        'emails/verify_account.txt',
        'emails/verify_account.html',
        token=token
    )

def send_email(subject, to, text_template, html_template, **kwargs):
    logging.debug(f'Sending email to {to} with subject: {subject}')
    logging.debug(f'MAILGUN_DOMAIN: {current_app.config["MAILGUN_DOMAIN"]}')
    logging.debug(f'MAILGUN_API_KEY: {current_app.config["MAILGUN_API_KEY"]}')
    logging.debug(f'MAILGUN_SMTP_LOGIN: {current_app.config["MAILGUN_SMTP_LOGIN"]}')
    
    text_body = render_template(text_template, **kwargs)
    html_body = render_template(html_template, **kwargs)

    response = requests.post(
        f"https://api.mailgun.net/v3/{current_app.config['MAILGUN_DOMAIN']}/messages",
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={"from": f"CyAware <{current_app.config['MAILGUN_SMTP_LOGIN']}>",
              "to": [to],
              "subject": subject,
              "text": text_body,
              "html": html_body})
    if response.status_code == 200:
        current_app.logger.info(f'Email sent to {to}: {subject}')
    else:
        current_app.logger.error(f'Failed to send email to {to}: {response.text}')
    return response

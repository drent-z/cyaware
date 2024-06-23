import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    MAIL_SERVER = os.getenv('MAILGUN_SMTP_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = int(os.getenv('MAILGUN_SMTP_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@demo.com')
    PAPERTRAIL_HOST = os.getenv('PAPERTRAIL_HOST', 'logs3.papertrailapp.com')
    PAPERTRAIL_PORT = int(os.getenv('PAPERTRAIL_PORT', 12345))

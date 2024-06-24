import os
import logging

logging.basicConfig(level=logging.DEBUG)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_hard_to_guess_string'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAILGUN_SMTP_SERVER')
    MAIL_PORT = int(os.getenv('MAILGUN_SMTP_PORT'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    MAILGUN_SMTP_LOGIN = os.getenv('MAILGUN_SMTP_LOGIN')
    PAPERTRAIL_HOST = os.getenv('PAPERTRAIL_HOST')
    PAPERTRAIL_PORT = int(os.getenv('PAPERTRAIL_PORT'))

logging.debug(f'MAILGUN_SMTP_LOGIN: {Config.MAILGUN_SMTP_LOGIN}')
logging.debug(f'MAILGUN_API_KEY: {Config.MAILGUN_API_KEY}')
logging.debug(f'MAILGUN_DOMAIN: {Config.MAILGUN_DOMAIN}')

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAILGUN_SMTP_SERVER')
    MAIL_PORT = int(os.getenv('MAILGUN_SMTP_PORT'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    PAPERTRAIL_HOST = os.getenv('PAPERTRAIL_HOST')
    PAPERTRAIL_PORT = int(os.getenv('PAPERTRAIL_PORT'))

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    emailLet's integrate the email verification and password reset functionalities properly into your existing Flask application structure.

### Project Structure

- `app/`
  - `__init__.py`
  - `models.py`
  - `users/`
    - `routes.py`
    - `forms.py`
    - `utils.py`
  - `templates/`
    - `email/`
      - `activate.html`
    - `reset_request.html`
    - `reset_password.html`

### `app/__init__.py`

Add Flask-Mail and necessary configurations for email handling.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from flask_mail import Mail
import redis
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()

# Use REDIS_TLS_URL for secure connection
redis_tls_url = os.getenv('REDIS_TLS_URL')

# Create Redis client using REDIS_TLS_URL and handle SSL certificates
redis_client = redis.from_url(redis_tls_url, ssl=True, ssl_cert_reqs='none')

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_tls_url,
    default_limits=["200 per day", "50 per hour"]
)

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app(config_class=os.getenv('FLASK_CONFIG_CLASS', 'app.config.Config')):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'You need to login to access this page.'
    login_manager.login_message_category = 'info'

    from app.users.routes import users
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/cyaware.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Papertrail logging
    papertrail_host = os.getenv('PAPERTRAIL_HOST', 'logs3.papertrailapp.com')
    papertrail_port = int(os.getenv('PAPERTRAIL_PORT', 12345))
    papertrail_handler = SysLogHandler(address=(papertrail_host, papertrail_port))
    papertrail_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(papertrail_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('CyAware startup')

    return app

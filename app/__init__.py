from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
import redis
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import os
import ssl
import certifi

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

# Setup Redis for rate limiting
redis_url = os.getenv('REDIS_URL', 'rediss://:p15879d51ee7c55ce1c05b88ce5dcd5aba46ff58dc872e3322774ccd866801bb8@ec2-34-195-55-195.compute-1.amazonaws.com:9150')

# Create an SSL context that uses the default CA certificates from certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Create Redis client with the custom SSL context
redis_client = redis.StrictRedis.from_url(redis_url, ssl_context=ssl_context)

limiter = Limiter(
    get_remote_address,
    storage_uri=redis_url,
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

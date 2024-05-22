from flask import Flask
from .models import db
from .routes import app as routes_app

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_app)

    return app

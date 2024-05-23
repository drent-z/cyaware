# app/app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from .models import User, QuizResult

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/content')
    def content():
        return render_template('content.html')

    @app.route('/quiz', methods=['GET', 'POST'])
    def quiz():
        if request.method == 'POST':
            # Process quiz submission
            pass
        return render_template('quiz.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('register.html')

    return app

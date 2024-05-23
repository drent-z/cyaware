from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from . import db, bcrypt
from .models import User

@current_app.route('/')
def index():
    return render_template('index.html')

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@current_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@current_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@current_app.route('/content')
@login_required
def content():
    return render_template('content.html')

@current_app.route('/quizzes')
@login_required
def quizzes():
    return render_template('quizzes.html')

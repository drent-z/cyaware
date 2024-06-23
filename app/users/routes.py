from flask import render_template, Blueprint, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, QuizResult, UserProgress
from app.users.forms import RegisterForm, LoginForm
from app.users.utils import save_picture
from sqlalchemy.exc import SQLAlchemyError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

users = Blueprint('users', __name__)
csrf = CSRFProtect()
limiter = Limiter(get_remote_address, app=None, default_limits=["200 per day", "50 per hour"])

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                flash('Username already exists. Please choose a different one.', 'danger')
                return render_template('register.html', title='Register', form=form)

            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already exists. Please choose a different one.', 'danger')
                return render_template('register.html', title='Register', form=form)

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('users.login'))
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            else:
                flash('Login unsuccessful. Please check email and password', 'danger')
        except SQLAlchemyError:
            flash('An error occurred while logging in. Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)

@csrf.exempt
@limiter.limit("5 per minute")
@users.route('/validate/<field>', methods=['POST'])
def validate_field(field):
    data = request.get_json()
    value = data.get('value', '')

    if field == 'username':
        user = User.query.filter_by(username=value).first()
        if user:
            return jsonify(valid=False, message='That username is taken. Please choose a different one.')
        else:
            return jsonify(valid=True, message='')

    elif field == 'email':
        user = User.query.filter_by(email=value).first()
        if user:
            return jsonify(valid=False, message='That email is taken. Please choose a different one.')
        else:
            return jsonify(valid=True, message='')

    return jsonify(valid=False, message='Invalid field.')

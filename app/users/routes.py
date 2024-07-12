from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, mail
from app.models import User
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm, ContactForm)
from app.users.utils import save_picture, send_reset_email, send_verification_email
from flask_mail import Message
import logging
import time
import requests
import os  # Ensure os is imported

users = Blueprint('users', __name__)

# Dictionary to store last verification email request time for each user
last_verification_request_time = {}

@users.route("/register", methods=['GET', 'POST'])
def register():
    current_app.logger.info("Accessed register page")
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.email} already authenticated, redirecting to main index")
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('Your account has been created! A verification email has been sent to your email address.', 'success')
        current_app.logger.info(f'New user registered: {user.email}')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    current_app.logger.info("Accessed login page")
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.email} already authenticated, redirecting to main index")
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if not user.verified:
                flash('Account not verified. Please check your email to verify your account.', 'warning')
                current_app.logger.info(f"User {user.email} attempted to login but is not verified")
                return render_template('login.html', title='Login', form=form, show_resend_button=True, email=form.email.data)
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                current_app.logger.info(f"User {user.email} logged in successfully")
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Login unsuccessful. Please check email and password', 'danger')
        current_app.logger.info("Login attempt failed")
    return render_template('login.html', title='Login', form=form, show_resend_button=False)

@users.route("/logout")
def logout():
    current_app.logger.info(f"User {current_user.email} logged out")
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    current_app.logger.info(f"Accessed account page for user {current_user.email}")
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        current_app.logger.info(f"Account updated for user {current_user.email}")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    current_app.logger.info("Accessed password reset request page")
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.email} already authenticated, redirecting to main index")
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        current_app.logger.info(f"Password reset email sent to {user.email}")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    current_app.logger.info(f"Accessed password reset page with token {token}")
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.email} already authenticated, redirecting to main index")
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        current_app.logger.warning("Invalid or expired password reset token")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        current_app.logger.info(f"Password updated for user {user.email}")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form, token=token)

@users.route('/validate/username', methods=['POST'])
def validate_username():
    data = request.get_json()
    username = data.get('value')
    user = User.query.filter_by(username=username).first()
    if user:
        current_app.logger.info(f'Username validation failed for: {username}')
        return jsonify({'valid': False, 'message': 'Username is already taken'}), 400
    current_app.logger.info(f'Username validation succeeded for: {username}')
    return jsonify({'valid': True, 'message': 'Username is available'}), 200

@users.route('/validate/email', methods=['POST'])
def validate_email():
    data = request.get_json()
    email = data.get('value')
    user = User.query.filter_by(email=email).first()
    if user:
        current_app.logger.info(f'Email validation failed for: {email}')
        return jsonify({'valid': False, 'message': 'Email is already taken'}), 400
    current_app.logger.info(f'Email validation succeeded for: {email}')
    return jsonify({'valid': True, 'message': 'Email is available'}), 200

@users.route("/verify/<token>")
def verify_token(token):
    current_app.logger.info(f"Accessed account verification page with token {token}")
    user = User.verify_verification_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        current_app.logger.warning("Invalid or expired verification token")
        return redirect(url_for('users.register'))
    user.verified = True
    db.session.commit()
    flash('Your account has been verified! You can now log in', 'success')
    current_app.logger.info(f"Account verified for user {user.email}")
    return redirect(url_for('users.login'))

@users.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    recaptcha_site_key = os.getenv('RECAPTCHA_SITE_KEY')
    recaptcha_secret_key = os.getenv('RECAPTCHA_SECRET_KEY')
    if form.validate_on_submit():
        recaptcha_token = request.form.get('recaptcha_token')
        project_id = current_app.config['GOOGLE_CLOUD_PROJECT_ID']
        recaptcha_action = 'contact'

        # Log form submission and reCAPTCHA token generation
        current_app.logger.info(f"Form submitted with reCAPTCHA token: {recaptcha_token}")

        # Create the request body
        request_body = {
            "event": {
                "token": recaptcha_token,
                "expectedAction": recaptcha_action,
                "siteKey": recaptcha_site_key,
            }
        }

        # Send the request to reCAPTCHA Enterprise API
        try:
            recaptcha_response = requests.post(
                f'https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments?key={recaptcha_secret_key}',
                json=request_body
            )
            recaptcha_response.raise_for_status()  # Raise HTTPError for bad responses
            current_app.logger.info("reCAPTCHA verification request sent successfully")
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error sending reCAPTCHA verification request: {e}")
            flash('Failed to verify reCAPTCHA. Please try again.', 'danger')
            return redirect(url_for('users.contact'))

        recaptcha_result = recaptcha_response.json()
        current_app.logger.info(f"reCAPTCHA response: {recaptcha_result}")

        if recaptcha_result.get('tokenProperties', {}).get('valid'):
            msg = Message(
                'Contact Form Submission',
                sender=form.email.data,
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg.body = f'''
            From: {form.name.data} <{form.email.data}>
            {form.message.data}
            '''
            try:
                mail.send(msg)
                current_app.logger.info(f'Message sent from {form.email.data}')
                flash('Your message has been sent. Thank you!', 'success')
            except Exception as e:
                current_app.logger.error(f'Failed to send message: {str(e)}')
                flash('Failed to send your message. Please try again later.', 'danger')
            return redirect(url_for('users.contact'))
        else:
            invalid_reason = recaptcha_result.get('tokenProperties', {}).get('invalidReason')
            current_app.logger.error(f"reCAPTCHA token validation failed: {invalid_reason}")
            flash('Failed to verify reCAPTCHA. Please try again.', 'danger')
    return render_template('contact.html', title='Contact', form=form, recaptcha_site_key=recaptcha_site_key)

@users.route("/resend_verification", methods=['POST'])
def resend_verification():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    current_app.logger.debug(f'Received resend verification request for email: {email}')
    if user and not user.verified:
        current_time = time.time()
        if user.id in last_verification_request_time:
            elapsed_time = current_time - last_verification_request_time[user.id]
            if elapsed_time < 300:  # 5 minutes
                current_app.logger.warning(f'Too soon to request another verification email for email: {email}')
                return jsonify({'message': 'You can only request a verification email once every 5 minutes.', 'status': 'warning'}), 429

        send_verification_email(user)
        last_verification_request_time[user.id] = current_time
        current_app.logger.info(f'Resent verification email to: {email}')
        return jsonify({'message': 'A new verification email has been sent to your email address.', 'status': 'success'}), 200
    else:
        current_app.logger.warning(f'Invalid resend verification attempt for email: {email}')
        return jsonify({'message': 'Invalid email or account already verified.', 'status': 'danger'}), 400

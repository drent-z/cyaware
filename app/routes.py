from flask import render_template, request, redirect, url_for, current_app as app
from . import db, bcrypt
from .models import User
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html', time=datetime.now().timestamp())

@app.route('/content')
def content():
    return render_template('content.html', time=datetime.now().timestamp())

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Process quiz submission
        pass
    return render_template('quiz.html', time=datetime.now().timestamp())

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
    return render_template('register.html', time=datetime.now().timestamp())

@app.route('/about')
def about():
    return render_template('about.html', time=datetime.now().timestamp())

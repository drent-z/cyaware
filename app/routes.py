from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user, LoginManager

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must be logged in to view this page.', 'warning')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/quizzes')
@login_required
def quizzes():
    return render_template('quizzes.html')

@app.route('/quiz/<int:id>')
@login_required
def quiz(id):
    return render_template('quiz.html', id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add your login logic here
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add your registration logic here
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

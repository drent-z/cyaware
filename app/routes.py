from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

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

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must be logged in to view this page.', 'warning')
    return redirect(url_for('login'))

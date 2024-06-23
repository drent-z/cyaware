from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from app.models import QuizResult

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        # Process quiz submission
        score = request.form.get('score')
        result = QuizResult(user_id=current_user.id, score=score)
        db.session.add(result)
        db.session.commit()
        flash('Quiz submitted successfully!', 'success')
        return redirect(url_for('main.quiz'))
    return render_template('quiz.html')

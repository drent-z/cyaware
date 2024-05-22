from flask import render_template, request, redirect, url_for, current_app as app, jsonify
from . import db, bcrypt
from .models import User, QuizResult, UserProgress

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    progress = UserProgress(
        user_id=data['user_id'],
        module_name=data['module_name'],
        progress=data['progress']
    )
    db.session.add(progress)
    db.session.commit()
    return jsonify({"message": "Progress updated"}), 201

@app.route('/api/progress/<int:user_id>', methods=['GET'])
def get_progress(user_id):
    progress = UserProgress.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'module_name': p.module_name,
        'progress': p.progress,
        'timestamp': p.timestamp
    } for p in progress])

@app.route('/api/quiz/results', methods=['POST'])
def submit_quiz_result():
    data = request.json
    quiz_result = QuizResult(
        user_id=data['user_id'],
        quiz_id=data['quiz_id'],
        score=data['score']
    )
    db.session.add(quiz_result)
    db.session.commit()
    return jsonify({"message": "Quiz result submitted"}), 201

@app.route('/api/quiz/results/<int:user_id>', methods=['GET'])
def get_quiz_results(user_id):
    results = QuizResult.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'quiz_id': r.quiz_id,
        'score': r.score,
        'timestamp': r.timestamp
    } for r in results])

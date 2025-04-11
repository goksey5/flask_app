from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Question, Score
from sqlalchemy import func

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username)
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('start_quiz'))
    return render_template('quiz_form.html')

@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    questions = Question.query.all()
    user = User.query.filter_by(username=session['username']).first()
    
    # Tüm zamanların en yüksek puanını al
    all_time_best = db.session.query(func.max(Score.score)).scalar() or 0
    
    # Kullanıcının en yüksek puanını al
    user_best = db.session.query(func.max(Score.score)).filter(Score.user_id == user.id).scalar() or 0
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(f'answer_{question.id}')
            if answer == question.correct_answer:
                score += 20
        
        new_score = Score(user_id=user.id, score=score)
        db.session.add(new_score)
        db.session.commit()
        
        session['last_score'] = score
        return redirect(url_for('result'))
    
    return render_template('quiz.html', 
                         questions=questions,
                         all_time_best=all_time_best,
                         user_best=user_best)

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=session['username']).first()
    
    # Tüm zamanların en yüksek puanını al
    all_time_best = db.session.query(func.max(Score.score)).scalar() or 0
    
    # Kullanıcının en yüksek puanını al
    user_best = db.session.query(func.max(Score.score)).filter(Score.user_id == user.id).scalar() or 0
    
    # Son alınan puanı al
    last_score = session.get('last_score', 0)
    
    return render_template(
        'result.html',
        username=session['username'],
        last_score=last_score,
        user_best=user_best,
        all_time_best=all_time_best
    )
@app.route('/show_scores')
def show_scores():
    # Tüm kullanıcıların skorlarını al
    scores = Score.query.join(User).add_columns(User.username, Score.score).all()
    
    # Skorları sıralayın (örneğin, yüksekten düşüğe doğru)
    scores = sorted(scores, key=lambda x: x.score, reverse=True)
    
    return render_template('scores.html', scores=scores)

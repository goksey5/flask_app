from flask import render_template, request, redirect, url_for, session
from app import app, db
from flask_quiz_app.models import User, Question, Score
from sqlalchemy import func

# Ana Sayfa: Kullanıcıdan isim al
@app.route('/')
def index():
    return render_template('index.html')

# Quiz Başlat (kullanıcı adı alındıktan sonra çalışır)
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0
        questions = Question.query.all()
        for question in questions:
            user_answer = request.form.get(f"answer_{question.id}")
            if user_answer and question.check_answer(user_answer):
                score += 1

        # Kullanıcıyı session'a kaydediyoruz
        username = "guest"  # Eğer kullanıcı oturum açmadıysa, guest olarak işlem yapılıyor
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        new_score = Score(user_id=user.id, score=score)
        db.session.add(new_score)
        db.session.commit()

        return render_template("result.html", score=score)

    else:
        questions = Question.query.all()
        return render_template("quiz.html", questions=questions)

# Quiz Sayfası (soruları gösterir ve quiz gönderimini alır)
@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = User.query.filter_by(username=session['username']).first()
    questions = Question.query.all()

    all_time_best = db.session.query(func.max(Score.score)).scalar() or 0
    user_best = db.session.query(func.max(Score.score)).filter(Score.user_id == user.id).scalar() or 0

    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(f'answer_{question.id}')
            if answer and answer.upper() == question.correct_answer.upper():
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

# Sonuç Sayfası
@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = User.query.filter_by(username=session['username']).first()
    all_time_best = db.session.query(func.max(Score.score)).scalar() or 0
    user_best = db.session.query(func.max(Score.score)).filter(Score.user_id == user.id).scalar() or 0
    last_score = session.get('last_score', 0)

    return render_template(
        'result.html',
        username=session['username'],
        last_score=last_score,
        user_best=user_best,
        all_time_best=all_time_best
    )

# Tüm Skorları Göster
@app.route('/show_scores')
def show_scores():
    scores = Score.query.join(User).add_columns(User.username, Score.score).all()
    scores = sorted(scores, key=lambda x: x.score, reverse=True)
    return render_template('scores.html', scores=scores)

from flask import render_template, request, redirect, url_for, session
from flask_quiz_app import app, db
from flask_quiz_app.models import User, Question, Score

# Ana Sayfa: Kullanıcıdan isim al
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("quiz"))
    return render_template("index.html")

# Quiz Başlat (kullanıcı adı alındıktan sonra çalışır)
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('start_quiz', username=user.username))
    return render_template('quiz_form.html')

# Quiz Sayfası (soruları gösterir ve quiz gönderimini alır)
@app.route('/quiz/<username>', methods=['GET', 'POST'])
def start_quiz(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    if request.method == 'POST':
        score = 0
        for question in Question.query.all():
            answer = request.form.get(f'answer_{question.id}')
            if answer == question.correct_answer:
                score += 1
        user_score = Score(user_id=user.id, score=score)
        db.session.add(user_score)
        db.session.commit()
        return redirect(url_for('quiz_results', username=user.username))
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions, user=user)

# Sonuç Sayfası
@app.route('/quiz/results/<username>')
def quiz_results(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_score = max(user.scores, key=lambda x: x.score, default=None)
        return render_template('result.html', user=user, user_score=user_score)
    return redirect(url_for('quiz'))

# Tüm Skorları Göster
@app.route('/show_scores')
def show_scores():
    scores = Score.query.join(User).add_columns(User.username, Score.score).all()
    scores = sorted(scores, key=lambda x: x.score, reverse=True)
    return render_template('scores.html', scores=scores)
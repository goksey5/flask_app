from flask import render_template, request, redirect, url_for, session
from flask_quiz_app import app, db
from flask_quiz_app.models import User, Question, Score

# Ana Sayfa: Kullanıcıdan isim al
@app.route('/')
def index():
    return render_template('index.html')

# Quiz Başlat (kullanıcı adı alındıktan sonra çalışır)
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Kullanıcının ismini al
        username = request.form.get('username')

        # Kullanıcıyı veritabanında ara (varsa)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        # Kullanıcıyı quiz sayfasına yönlendir
        return redirect(url_for('start_quiz', username=user.username))  # Quiz sayfasına yönlendir

    return render_template('quiz_form.html')  # Kullanıcıdan adını alacak formu göster

# Quiz Sayfası (soruları gösterir ve quiz gönderimini alır)
@app.route('/quiz/<username>', methods=['GET', 'POST'])
def start_quiz(username):
    # Kullanıcıyı username ile veritabanında ara
    user = User.query.filter_by(username=username).first()
    
    # Eğer kullanıcı veritabanında yoksa, yeni bir kullanıcı ekle
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    # Sorulara göre işlem yapılacaksa
    if request.method == 'POST':
        score = 0
        # Soruları kontrol et ve skoru hesapla
        for question in Question.query.all():
            answer = request.form.get(f'answer_{question.id}')
            if answer == question.correct_answer:
                score += 1
        
        # Eğer yeni skor eski skordan büyükse, skoru güncelle
        user_score = Score(user_id=user.id, score=score)
        db.session.add(user_score)
        db.session.commit()

        # Sonuçları göster
        return redirect(url_for('quiz_results', username=user.username))

    # Soruları al
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions, user=user)  # user gönderiyoruz

# Sonuç Sayfası
@app.route('/quiz/results/<username>')
def quiz_results(username):
    # Kullanıcıyı username ile veritabanından al
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

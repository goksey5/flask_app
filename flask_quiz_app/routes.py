from flask import Flask, render_template, request, redirect, url_for, session
from flask_quiz_app import app,db
from flask_quiz_app.models import User, Question, Score
from flask_sqlalchemy import SQLAlchemy

app = Flask('main', __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)



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
        user = username.query.filter_by(name=username).first()
        if not user:
            user = username(name=username)
            db.session.add(user)
            db.session.commit()

        # Kullanıcıyı quiz sayfasına yönlendir
        return redirect(url_for('start_quiz', username=user.name))  # Quiz sayfasına yönlendir

    return render_template('quiz_form.html')  # Kullanıcıdan adını alacak formu göster

# Quiz Sayfası (soruları gösterir ve quiz gönderimini alır)
@app.route('/quiz/<username>', methods=['GET', 'POST'])
def start_quiz(username):
    # Kullanıcıyı username ile veritabanında ara
    user_score = Score.query.filter_by(username=username).first()  # username üzerinden sorgulama
    
    # Eğer kullanıcı veritabanında yoksa, yeni bir kullanıcı ekle
    if not user_score:
        user_score = Score(username=username, score=0)  # İlk skoru 0 olarak ekliyoruz
        db.session.add(user_score)
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
        if score > user_score.score:
            user_score.score = score
            db.session.commit()  # Skoru kaydediyoruz

        # Sonuçları göster
        return redirect(url_for('quiz_results', username=user_score.username))

    # Soruları al
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions, user=user_score)  # user_score gönderiyoruz


# Sonuç Sayfası
@app.route('/quiz/results/<username>')
def quiz_results(username):
    # Kullanıcıyı username ile veritabanından al
    user_score = Score.query.filter_by(username=username).first()  
    if user_score:
        print(f"User Name: {user_score.username}, Highest Score: {user_score.score}")
        return render_template('result.html', user=user_score)
    return redirect(url_for('quiz'))


@app.route('/')
def index():
    return render_template('index.html')  # Index sayfasını göster

# Tüm Skorları Göster
@app.route('/show_scores')
def show_scores():
    scores = Score.query.join(User).add_columns(User.username, Score.score).all()
    scores = sorted(scores, key=lambda x: x.score, reverse=True)
    return render_template('scores.html', scores=scores)

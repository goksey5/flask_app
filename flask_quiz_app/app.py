from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Güvenli veritabanı yolu ayarı
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'secret_key'

# SQLite veritabanı yolu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı ve migrate işlemleri
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelleri içe aktar
from models import User, Question, Score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    # Kullanıcı adı alındı
    username = request.form.get('username')
    # Kullanıcı veritabanında var mı kontrol edelim
    user = User.query.filter_by(username=username).first()

    if not user:
        # Eğer kullanıcı yoksa, yeni kullanıcı ekleyelim
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    # Kullanıcıyı session'a kaydedelim
    session['user_id'] = user.id
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    # Veritabanından soruları alalım
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    # Kullanıcının cevaplarını alalım
    answers = request.form.to_dict()  # Cevapları alıyoruz
    user_id = session.get('user_id')

    # Skoru hesaplayalım
    score = 0
    for question_id, user_answer in answers.items():
        question_id = question_id.split('_')[1]  # answer_{question_id} formatını ayarlıyoruz
        question = Question.query.get(question_id)
        if question.check_answer(user_answer):
            score += 1

    # Skoru veritabanına kaydedelim
    user = User.query.get(user_id)
    new_score = Score(score=score, user_id=user.id)
    db.session.add(new_score)
    db.session.commit()

    return redirect(url_for('result', score=score))

@app.route('/result')
def result():
    score = request.args.get('score')
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)

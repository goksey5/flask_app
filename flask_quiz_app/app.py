from flask import Flask, render_template, request, redirect, url_for, session
from flask_quiz_app.extensions import db, migrate  # extensions'dan db ve migrate import ediyoruz
from flask_quiz_app.models import User, Question, Score
from dotenv import load_dotenv
import os

# Çevresel yapılandırmayı .env dosyasından alalım
load_dotenv()

# Güvenli veritabanı yolu ayarı
basedir = os.path.abspath(os.path.dirname(__file__))

# Uygulama oluşturuluyor
app = Flask(__name__)

# SECRET_KEY'yi .env dosyasından alıyoruz
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı ve migrate işlemleri
db.init_app(app)
migrate.init_app(app, db)  # migrate'i app ile başlatıyoruz

# Rotalar
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
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
    answers = request.form.to_dict()  # Cevapları alıyoruz
    user_id = session.get('user_id')

    score = 0
    for question_id, user_answer in answers.items():
        question_id = question_id.split('_')[1]  # answer_{question_id} formatını ayarlıyoruz
        question = Question.query.get(question_id)
        if question.check_answer(user_answer):  # Eğer doğruysa skoru arttır
            score += 1

    # Skoru veritabanına kaydedelim
    user = User.query.get(user_id)
    new_score = Score(score=score, user_id=user.id)
    db.session.add(new_score)
    db.session.commit()

    return redirect(url_for('result', score=score))

@app.route('/result', methods=['GET'])
def result():
    score = request.args.get('score')
    user_id = session.get('user_id')
    username = User.query.get(user_id).username if user_id else 'Anonim'
    
    return render_template('result.html', score=score, username=username)

@app.route('/results')
def results():
    scores = Score.query.order_by(Score.id.desc()).all()
    return render_template('scores.html', scores=scores)

@app.route('/show_scores')
def show_scores():
    scores = Score.query.order_by(Score.id.desc()).all()
    return render_template('scores.html', scores=scores)

# Uygulama çalıştırma
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluşturur
    app.run(debug=True)

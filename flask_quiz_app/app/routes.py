from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Question, Score

# Quiz formu
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Kullanıcının ismini al
        username = request.form.get('username')

        # Kullanıcıyı veritabanında ara (varsa)
        user = Score.query.filter_by(username=username).first()
        if not user:
            user = Score(username=username, score=0)
            db.session.add(user)
            db.session.commit()

        # Kullanıcıyı quiz sayfasına yönlendir
        return redirect(url_for('start_quiz', username=user.username))  # Quiz sayfasına yönlendir

    return render_template('quiz_form.html')  # Kullanıcıdan adını alacak formu göster


# Quiz'i başlatma
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
            if answer == question.answer:
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


# Sonuçları gösterme
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

@app.route('/scores')
def show_scores():
    scores = Score.query.all()  # Tüm skorları al
    return render_template('scores.html', scores=scores)  # Skor sayfasını göster
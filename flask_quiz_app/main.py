from app import app, db  # app.py'den import yapıyoruz
from flask import render_template, request, redirect, url_for, session
from app.models import User, Question, Score  # Modelleri import ettik

# Ana sayfa
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["username"] = request.form["username"]  # Kullanıcı adını oturuma kaydet
        return redirect(url_for("quiz"))
    return render_template("index.html")

# Sınav sayfası
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "username" not in session:
        return redirect(url_for("index"))

    user = User.query.filter_by(username=session["username"]).first()
    questions = Question.query.all()

    # En yüksek skoru al
    best_score = Score.query.filter_by(user_id=user.id).with_entities(db.func.max(Score.score)).scalar()

    if request.method == "POST":
        score = 0
        for question in questions:
            answer = request.form.get(f"answer_{question.id}")
            if answer == question.correct_answer:
                score += 1

        new_score = Score(score=score, user_id=user.id)
        db.session.add(new_score)
        db.session.commit()

        session["score"] = score
        return redirect(url_for("result"))

    return render_template("quiz.html", questions=questions, best_score=best_score)

# Sonuç sayfası
@app.route("/result")
def result():
    if "username" not in session or "score" not in session:
        return redirect(url_for("index"))  # Eğer session yoksa, ana sayfaya yönlendir.

    user = User.query.filter_by(username=session["username"]).first()
    best_score = Score.query.filter_by(user_id=user.id).with_entities(db.func.max(Score.score)).scalar()

    return render_template("result.html", score=session["score"], best_score=best_score)

# Geliştirici hakkında bilgi
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

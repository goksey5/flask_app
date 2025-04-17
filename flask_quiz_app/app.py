from flask import Flask, render_template, request, redirect, url_for, session

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app.secret_key = "supersecretkey"  # Kullanıcı oturumu için

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect("quiz.db")
    conn.row_factory = sqlite3.Row
    return conn

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
    conn = get_db_connection()
    questions = conn.execute("SELECT * FROM questions").fetchall()
    
    # En yüksek skoru al
    best_score = conn.execute(
        "SELECT MAX(score) AS best_score FROM scores WHERE username = ?",
        (session["username"],)
    ).fetchone()["best_score"]
    conn.close()
    
    if request.method == "POST":
        score = 0
        for question in questions:
            answer = request.form.get(f"answer_{question['id']}")
            if answer == question["correct_answer"]:
                score += 1

        # Kullanıcının en yüksek puanını kaydet
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO scores (username, score) VALUES (?, ?)",
            (session["username"], score),
        )
        conn.commit()
        conn.close()

        session["score"] = score
        return redirect(url_for("result"))

    return render_template("quiz.html", questions=questions, best_score=best_score)



# Sonuç sayfası
@app.route("/result")
def result():
    conn = get_db_connection()
    best_score = conn.execute(
        "SELECT MAX(score) AS best_score FROM scores WHERE username = ?",
        (session["username"],),
    ).fetchone()["best_score"]
    
    conn.close()
    return render_template("result.html", score=session["score"], best_score=best_score)
    
#quize best score u yolla....

#---------------------------------

# Geliştirici hakkında bilgi
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

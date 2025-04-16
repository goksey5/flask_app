from flask_quiz_app import app, db
from flask import render_template, request, redirect, url_for, session
from flask_quiz_app.models import Score, Question

# Geliştirici hakkında bilgi
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
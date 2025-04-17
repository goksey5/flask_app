from flask_sqlalchemy import SQLAlchemy
from app import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)  # unique=True ile kullanıcı adı benzersiz olmalı
    score = db.Column(db.Integer, nullable=False, default=0)  # Başlangıç skoru 0 olarak kabul ediyorum

    def __repr__(self):
        return f"User('{self.username}', '{self.score}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    options = db.Column(db.Text, nullable=False)  # Seçenekler virgülle ayrılabilir

class Answer(db.Model):  # İsteğe bağlı
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_given = db.Column(db.String(100))

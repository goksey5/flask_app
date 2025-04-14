# models.py

from datetime import datetime
from flask_quiz_app.extensions import db, migrate

# Kullanıcı Modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    scores = db.relationship('Score', back_populates='user', lazy=True)

    def get_highest_score(self):
        if not self.scores:
            return 0
        return max(score.score for score in self.scores)

    def __repr__(self):
        return f'<User {self.username}>'

# Soru Modeli
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

    def check_answer(self, answer):
        return answer.lower() == self.correct_answer.lower()

    def __repr__(self):
        return f'<Question {self.text[:20]}...>'

# Skor Modeli
class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='scores')


    def __repr__(self):
        return f'<Score {self.score}>'


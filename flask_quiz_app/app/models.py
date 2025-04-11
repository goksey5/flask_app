from datetime import datetime
from app import db  # db'yi burada doğru şekilde import ediyoruz

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    scores = db.relationship('Score', backref='user', lazy=True)

    def get_highest_score(self):
        if not self.scores:
            return 0
        return max(score.score for score in self.scores)

    def __repr__(self):
        return f'<User {self.username}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    
    def check_answer(self, answer):
        return answer.lower() == self.correct_answer.lower()
    
    def __repr__(self):
        return f'<Question {self.question_text[:20]}...>'

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    quiz_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Score {self.score}>'

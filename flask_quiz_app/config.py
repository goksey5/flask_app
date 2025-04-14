# flask_quiz_app/config.py

import os
from dotenv import load_dotenv

# FLASK_QUIZ dizinindeki .env dosyasını yükle
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))  # .env dosyasının doğru yoldan yüklenmesi sağlanır

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)

    db_path = os.getenv('DATABASE_URL') or os.path.join(basedir, 'flask_quiz_app', 'quiz.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False




# flask_quiz_app/config.py

import os
from dotenv import load_dotenv

# .env dosyasını yükle
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)

    # DATABASE_URL doğrudan URI olarak kullanılmalı
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'flask_quiz_app', 'quiz.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

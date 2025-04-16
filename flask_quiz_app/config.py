import os
from dotenv import load_dotenv

# .env dosyasını yükle
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)

    # Önce .env dosyasındaki DATABASE_URL'yi kullan, yoksa varsayılan olarak local sqlite
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'quiz.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


# config.py
import os
from dotenv import load_dotenv

# .env dosyasındaki çevresel değişkenleri yükle
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///instance/quiz.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



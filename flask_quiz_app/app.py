from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Güvenli veritabanı yolu ayarı
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'secret_key'

# SQLite veritabanı yolu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı ve migrate işlemleri
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelleri içe aktar
from models import User, Question, Score

# Route'ları dahil et (çok önemli!)
import routes

# Geliştirme ortamında sunucuyu başlat
if __name__ == '__main__':
    app.run(debug=True)

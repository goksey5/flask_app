from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Flask uygulamasını oluştur
app = Flask(__name__)

# Veritabanı yolunu belirle
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../instance/quiz.db')

# Yapılandırma
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db = SQLAlchemy(app)

# Route'ları import et
from app import routes, models

# Veritabanını oluştur
with app.app_context():
    db.create_all()
# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask uygulaması oluşturuluyor
app = Flask(__name__)

# Veritabanı yolunu belirle
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'quiz.db')  # Veritabanı dosyası 'instance/quiz.db'

# Yapılandırmalar
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

# Veritabanı ve migrasyon nesneleri oluşturuluyor
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modeller içe aktarılıyor (db tanımlandıktan sonra!)
from app.models import User, Question, Score

# Ana çalışma bloğu
if __name__ == "__main__":
    app.run(debug=True)


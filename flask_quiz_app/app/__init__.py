from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask uygulaması ve veritabanı nesnelerini oluştur
app = Flask(__name__)

# Veritabanı yolunu belirt
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'quiz.db')  # Veritabanı dosyasının yolu

# Yapılandırma
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı nesnesi
db = SQLAlchemy(app)

# Uygulama rotalarını ve modelleri içe aktar
from app import routes, models

# Veritabanını oluştur
with app.app_context():
    db.create_all()  # Veritabanı tablolarını oluştur


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Uygulama nesnesi
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Uygulama ile ilgili diğer ayarlar veya importlar buraya eklenebilir
from app import routes  # routes.py dosyasını buraya import et



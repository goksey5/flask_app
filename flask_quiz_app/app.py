from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_quiz_app.config import Config

# Uygulama ve veritabanı bağlantılarını oluşturma
app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy ve Migrate'ı uygulamaya bağlama
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_quiz_app import routes  # routes.py içeriği





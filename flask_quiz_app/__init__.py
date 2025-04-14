# flask_quiz_app/__init__.py

from flask import Flask
from flask_quiz_app.config import Config
from flask_migrate import Migrate
from flask_quiz_app.extensions import db, migrate

def create_app():
    app = Flask(__name__)

    # Konfigürasyon ayarları
    app.config.from_object(Config)

    # Uzantıları başlat
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint'leri kaydet
    from flask_quiz_app.routes import main
    app.register_blueprint(main)

    return app

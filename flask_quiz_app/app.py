# flask_quiz_app/app.py

from flask import Flask
from flask_quiz_app.config import Config
from flask_quiz_app.extensions import db, migrate
from flask_quiz_app.routes import main  # Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    app.register_blueprint(main)

    return app






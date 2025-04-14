from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Uzantıları başlatıyoruz
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Uygulama konfigürasyonlarını buraya ekleyebilirsiniz
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Uzantıları uygulamaya bağlıyoruz
    db.init_app(app)
    migrate.init_app(app, db)

    # Diğer bileşenler
    with app.app_context():
        import flask_quiz_app.routes  # Routes'i burada dahil ediyoruz

    return app

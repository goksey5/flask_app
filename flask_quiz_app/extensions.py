from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Veritabanı bağlantısı için SQLAlchemy nesnesi
db = SQLAlchemy()

# Flask-Migrate nesnesi
migrate = Migrate()



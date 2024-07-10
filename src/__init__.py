from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configurations

db = SQLAlchemy()


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    db.init_app(app)

    from .auth import auth
    from .views import views
    from .models import Usuario, Medico, Post, Comentario
    from .models import Favorito, LerMaisTarde, Report

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()

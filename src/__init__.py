import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect

from config import configurations
from .models import db, migrate
from .auth import auth, bcrypt, login_manager
from .views import views

bootstrap = Bootstrap5()
csrf = CSRFProtect()


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    # Inicialização de extensões
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    # Registro de Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Inicia o logger em prod
    if not app.debug:
        configure_logging(app)

    return app


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()


def configure_logging(app: Flask) -> None:
    file_handler = RotatingFileHandler(
        'logs/flask_app.log', maxBytes=10240, backupCount=10)

    # Formatter com informação de timezone
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S %p %z'  # ISO 8601
    )
    file_handler.setFormatter(formatter)

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask App Startup')

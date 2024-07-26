import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from .config import configurations
from .extensions import db, init_extensions
from .views import views, auth


def create_app(config='default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    # Inicialização de extensões
    init_extensions(app=app)

    # Registro de Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Inicia o logger em prod/testing
    if not app.debug:
        configure_logging(app)

    return app


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()


def configure_logging(app: Flask) -> None:
    if not os.path.exists('logs'):
        os.makedirs('logs')
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

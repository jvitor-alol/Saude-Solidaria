import pytest

from app import create_app
from app.models import Usuario
from app.extensions import db, bcrypt


@pytest.fixture(scope='module')
def app():
    app = create_app(config='testing')

    # Desabilita a proteção CSRF para testes
    app.config['WTF_CSRF_ENABLED'] = False

    yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def logged_in_client(client, app):
    with app.app_context():
        generate_test_user()

        client.post('/auth/login', data={
            'email': 'test@example.com',
            'senha': 'password123'
        }, follow_redirects=True)
    return client


def generate_test_user() -> None:
    hashed_password = bcrypt.generate_password_hash('password123') \
        .decode('utf-8')
    user = Usuario(
        nome='Test',
        sobrenome='User',
        nome_usuario='testuser',
        email='test@example.com',
        senha=hashed_password,
        tipo_usuario='comum'
    )
    db.session.add(user)
    db.session.commit()

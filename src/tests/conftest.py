import pytest

from app import create_app
from app.models import Usuario
from app.extensions import db, bcrypt


# Fixture para criar e configurar o app
@pytest.fixture(scope='module')
def app():
    app = create_app(config='testing')

    # Desabilita a proteção CSRF para testes
    app.config['WTF_CSRF_ENABLED'] = False

    yield app


# Fixture para o cliente de teste
@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


# Fixture para configurar e limpar o banco de dados
@pytest.fixture(scope='function', autouse=True)
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


# Fixture para usuário comum autenticado
@pytest.fixture
def logged_in_client(client, app):
    with app.app_context():
        generate_test_user()

        client.post('/auth/login', data={
            'email': 'test@example.com',
            'senha': 'password123'
        }, follow_redirects=True)
    return client


# Fixture para médico autenticado
@pytest.fixture
def logged_in_md(client, app):
    with app.app_context():
        generate_test_user(tipo_usuario='medico')

        client.post('/auth/login', data={
            'email': 'test@example.com',
            'senha': 'password123'
        }, follow_redirects=True)
    return client


def generate_test_user(tipo_usuario='comum') -> None:
    hashed_password = bcrypt.generate_password_hash('password123') \
        .decode('utf-8')
    user = Usuario(
        nome='Test',
        sobrenome='User',
        nome_usuario='testuser',
        email='test@example.com',
        senha=hashed_password,
        tipo_usuario=tipo_usuario
    )
    db.session.add(user)
    db.session.commit()

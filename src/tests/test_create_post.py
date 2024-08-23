import pytest
from app import create_app
from app.models import Usuario, Post
from app.extensions import db, bcrypt

@pytest.fixture(scope='module')
def app():
    app = create_app(config='testing')
    app.config['WTF_CSRF_ENABLED'] = False
    yield app

@pytest.fixture(scope='function', autouse=True)
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def logged_in_client(client):
    hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
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

    client.post('/auth/login', data={
        'email': 'test@example.com',
        'senha': 'password123'
    }, follow_redirects=True)
    
    return client

def test_create_post(logged_in_client):
    autor = Usuario.query.first()
    post = Post(
        titulo='Novo Post',
        conteudo='Conteúdo do post',
        categoria='Categoria Exemplo',
        autor_id=autor.id
    )
    db.session.add(post)
    db.session.commit()

    post_in_db = Post.query.get(post.id)
    assert post_in_db is not None
    assert post_in_db.titulo == 'Novo Post'
    assert post_in_db.conteudo == 'Conteúdo do post'
    assert post_in_db.categoria == 'Categoria Exemplo'
    assert post_in_db.autor_id == autor.id
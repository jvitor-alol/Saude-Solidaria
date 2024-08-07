import pytest
import io
from app import create_app
from app.models import Usuario
from app.extensions import db, bcrypt
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os

@pytest.fixture(scope='module')
def app():
    app = create_app(config='testing')

    # Desabilita a proteção CSRF para testes
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static')
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

    # Certifique-se de que o diretório de upload exista
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'success': f'File {filename} uploaded successfully'}), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400

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

# Testes adicionais
def test_upload_no_file_part(client, logged_in_client):
    response = logged_in_client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'No file part' in response.json['error']

def test_upload_no_selected_file(client, logged_in_client):
    data = {
        'image': (io.BytesIO(b''), '')  # Arquivo vazio e nome vazio
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'No selected file' in response.json['error']

def test_upload_invalid_file_type(client, logged_in_client):
    data = {
        'image': (io.BytesIO(b'Invalid content'), 'test.txt')  # Arquivo de texto, tipo não permitido
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'Invalid file type' in response.json['error']

def test_upload_large_file(client, logged_in_client):
    large_content = b'a' * (10 * 1024 * 1024 + 1)  # Arquivo maior que 10MB
    data = {
        'image': (io.BytesIO(large_content), 'large_image.png')
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 413  # 413 Payload Too Large
    # assert 'File too large' in response.json['error']  # Descomente se você adicionar uma mensagem de erro específica

def test_successful_registration(client):
    response = client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    assert response.status_code == 200
    assert 'User registered successfully' in response.data.decode('utf-8')

def test_duplicate_registration(client):
    # Primeiro registro
    client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    # Tentativa de registro duplicado
    response = client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    assert response.status_code == 400
    assert 'Email or username already exists' in response.json['error']

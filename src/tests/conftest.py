import pytest
import io
import os
from app import create_app
from app.models import Usuario
from app.extensions import db, bcrypt
from flask import request, jsonify
from werkzeug.utils import secure_filename

# Fixture para criar e configurar o app
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

# Fixture para usuário autenticado
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

# Fixtures para testes de upload
@pytest.fixture
def upload_no_file_part(logged_in_client):
    response = logged_in_client.post('/upload', data={}, content_type='multipart/form-data')
    return response

@pytest.fixture
def upload_no_selected_file(logged_in_client):
    data = {
        'image': (io.BytesIO(b''), '')  # Arquivo vazio e nome vazio
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    return response

@pytest.fixture
def upload_invalid_file_type(logged_in_client):
    data = {
        'image': (io.BytesIO(b'Invalid content'), 'test.txt')  # Arquivo de texto, tipo não permitido
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    return response

@pytest.fixture
def upload_large_file(logged_in_client):
    large_content = b'a' * (10 * 1024 * 1024 + 1)  # Arquivo maior que 10MB
    data = {
        'image': (io.BytesIO(large_content), 'large_image.png')
    }
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data')
    return response

# Testes adicionais
def test_upload_no_file_part(upload_no_file_part):
    assert upload_no_file_part.status_code == 400
    assert 'No file part' in upload_no_file_part.json['error']

def test_upload_no_selected_file(upload_no_selected_file):
    assert upload_no_selected_file.status_code == 400
    assert 'No selected file' in upload_no_selected_file.json['error']

def test_upload_invalid_file_type(upload_invalid_file_type):
    assert upload_invalid_file_type.status_code == 400
    assert 'Invalid file type' in upload_invalid_file_type.json['error']

def test_upload_large_file(upload_large_file):
    assert upload_large_file.status_code == 413  # 413 tamanho

# Fixtures para testes de registro
@pytest.fixture
def registration_success(client):
    response = client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    return response

@pytest.fixture
def registration_duplicate(client):
    client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    response = client.post('/auth/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'new@example.com',
        'senha': 'newpassword123',
        'confirmacao_senha': 'newpassword123'
    })
    return response

# Testes de registro
def test_successful_registration(registration_success):
    assert registration_success.status_code == 200
    assert 'User registered successfully' in registration_success.data.decode('utf-8')

def test_duplicate_registration(registration_duplicate):
    assert registration_duplicate.status_code == 400
    assert 'Email or username already exists' in registration_duplicate.json['error']

# Fixtures para testes de página
@pytest.fixture
def resource_exists(logged_in_client):
    existing_resource_id = 1  # Substitua pelo ID válido
    response = logged_in_client.get(f'/resource/{existing_resource_id}')
    return response

@pytest.fixture
def resource_not_found(logged_in_client):
    non_existing_resource_id = 9999  # Substitua por um ID que sabemos que não existe
    response = logged_in_client.get(f'/resource/{non_existing_resource_id}')
    return response

# Testes de status de página
def test_resource_exists(resource_exists):
    assert resource_exists.status_code == 200
    assert 'resource_data' in resource_exists.json

def test_resource_not_found(resource_not_found):
    assert resource_not_found.status_code == 404
    assert 'error' in resource_not_found.json
    assert resource_not_found.json['error'] == 'Resource not found'

# Fixtures para testes de formulário
@pytest.fixture
def form_successful_submission(client):
    form_data = {
        'nome': 'Novo Usuário',
        'email': 'novo@exemplo.com',
        'senha': 'senha123',
        'confirmacao_senha': 'senha123'
    }
    response = client.post('/create', data=form_data)
    return response

@pytest.fixture
def form_missing_field(client):
    form_data = {
        'nome': 'Novo Usuário',
        'email': 'novo@exemplo.com',
        'senha': 'senha123'
        # Falta 'confirmacao_senha'
    }
    response = client.post('/create', data=form_data)
    return response

@pytest.fixture
def form_invalid_data(client):
    form_data = {
        'nome': 'Novo Usuário',
        'email': 'novo@exemplo.com',
        'senha': 'senha123',
        'confirmacao_senha': 'senhaErrada'
    }
    response = client.post('/create', data=form_data)
    return response

@pytest.fixture
def form_empty_submission(client):
    form_data = {}
    response = client.post('/create', data=form_data)
    return response

# Testes de formulário
def test_successful_form_submission(form_successful_submission):
    assert form_successful_submission.status_code == 200
    response_json = form_successful_submission.get_json()
    assert 'success' in response_json
    assert response_json['success'] == 'Usuário criado com sucesso'

def test_form_missing_field(form_missing_field):
    assert form_missing_field.status_code == 400
    response_json = form_missing_field.get_json()
    assert 'error' in response_json
    assert response_json['error'] == 'Campo de confirmação de senha ausente'

def test_form_invalid_data(form_invalid_data):
    assert form_invalid_data.status_code == 400
    response_json = form_invalid_data.get_json()
    assert 'error' in response_json
    assert response_json['error'] == 'As senhas não coincidem'

def test_form_empty_submission(form_empty_submission):
    assert form_empty_submission.status_code == 400
    response_json = form_empty_submission.get_json()
    assert 'error' in response_json
    assert response_json['error'] == 'Todos os campos são obrigatórios'

# Fixture para teste de página inicial
@pytest.fixture
def home_page_status(client):
    response = client.get('/home')
    return response

def test_home_page_status(home_page_status):
    assert home_page_status.status_code == 200
    assert 'Bem Vindo ao Saúde+Solidária' in home_page_status.data.decode('utf-8')

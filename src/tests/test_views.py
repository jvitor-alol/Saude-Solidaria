from app.models import Usuario


def test_home(client, logged_in_client):
    response = client.get('/')
    assert '<title>Saúde + Solidária</title>' in response.data.decode('utf-8')
    response = client.get('/home')
    assert '<title>Saúde + Solidária</title>' in response.data.decode('utf-8')

    response = logged_in_client.get('/')
    assert '<title>Saúde + Solidária</title>' in response.data.decode('utf-8')
    response = logged_in_client.get('/home')
    assert '<title>Saúde + Solidária</title>' in response.data.decode('utf-8')


def test_register_user(client, app):
    response = client.post('/register', data={
        'nome': 'New',
        'sobrenome': 'User',
        'nome_usuario': 'newuser',
        'email': 'newuser@example.com',
        'senha': 'password123',
        'confirmar_senha': 'password123',
        'tipo_usuario': 'comum'
    }, follow_redirects=True)

    # Verifique o status da resposta e o conteúdo
    with app.app_context():
        assert response.status_code == 200
        assert b"Conta criada para" in response.data

        # Verifique se o usuário foi adicionado ao banco de dados
        user = Usuario.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.nome_usuario == 'newuser'
        assert user.email == 'newuser@example.com'


def test_account(logged_in_client):
    response = logged_in_client.get('/account')
    assert '<title>Saúde + Solidária • Conta</title>' in response.data \
        .decode('utf-8')
    assert b'Bem-vindo(a), Test User' in response.data

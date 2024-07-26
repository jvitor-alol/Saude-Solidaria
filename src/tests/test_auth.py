from .conftest import generate_test_user


def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_successful_login(client, app):
    with app.app_context():
        generate_test_user()

    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'senha': 'password123',
        'lembre_de_mim': False
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logout' in response.data


def test_unsuccessful_login(client):
    response = client.post('/auth/login', data={
        'email': 'wrong@example.com',
        'senha': 'wrongpassword',
        'lembre_de_mim': False
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login falhou. Verifique seu email e senha.' in response.data


def test_login_redirect_if_authenticated(logged_in_client):
    response = logged_in_client.get('/auth/login', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data

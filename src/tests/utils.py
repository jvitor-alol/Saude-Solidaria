from app.models import Usuario
from app.extensions import db, bcrypt


def generate_test_user(tipo_usuario='comum'):
    hashed_password = bcrypt.generate_password_hash(
        'password123').decode('utf-8')
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

from src import create_app


def test_database_connection():
    app = create_app(config='development')
    with app.app_context():
        try:
            from flask_sqlalchemy import SQLAlchemy
            db = SQLAlchemy()
            db.init_app(app)
            db.engine.execute('SELECT 1')
            print('Conexão com o banco de dados estabelecida com sucesso!')
        except Exception as e:
            print(f'Erro ao conectar ao banco de dados: {str(e)}')


if __name__ == '__main__':
    test_database_connection()

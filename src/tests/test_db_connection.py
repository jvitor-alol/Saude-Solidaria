from app import create_app, db
from sqlalchemy.sql import text


def test_database_connection():
    app = create_app(config='testing')
    with app.app_context():
        try:
            app.logger.info("Teste de conexão com db")
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            app.logger.info(
                "Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            app.logger.info(f"Erro ao conectar ao banco de dados: {str(e)}")


if __name__ == '__main__':
    test_database_connection()

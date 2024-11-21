from datetime import datetime
from .. import db  # Supondo que você esteja utilizando o SQLAlchemy para o banco de dados

class Historico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    descricao = db.Column(db.String(255))

    def __repr__(self):
        return f"<Historico {self.id}>"

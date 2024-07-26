from ..extensions import db


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self) -> str:
        return f"Tag({self.id=}, {self.nome=})"

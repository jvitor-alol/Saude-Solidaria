from datetime import datetime, timezone

from .setup import db


class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    nota_geral = db.Column(db.Integer, default=0)
    num_votos = db.Column(db.Integer, default=0)
    data_comentario = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultima_atualizacao = db.Column(db.DateTime(timezone=True))
    editado = db.Column(db.Boolean, default=False)
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(
            self, conteudo, autor_id, post_id, nota_geral=0, num_votos=0,
            data_comentario=None, ultima_atualizacao=None, editado=False):
        self.conteudo = conteudo
        self.nota_geral = nota_geral
        self.num_votos = num_votos
        self.data_comentario = data_comentario if data_comentario \
            else datetime.now(timezone.utc)
        self.ultima_atualizacao = ultima_atualizacao
        self.editado = editado
        self.autor_id = autor_id
        self.post_id = post_id

    def __repr__(self) -> str:
        return f"Comentario({self.id=}, {self.autor_id=}, {self.post_id=})"

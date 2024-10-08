from datetime import datetime, timezone

from .relacionamentos import posts_tags
from ..extensions import db

DEFAULT_COVER_PATH = 'https://via.placeholder.com/1920x500'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    foto_cover = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_COVER_PATH)
    media_estrelas = db.Column(db.Float, default=0)
    num_votos = db.Column(db.Integer, default=0)
    data_publicacao = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultima_atualizacao = db.Column(db.DateTime(timezone=True))
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)

    # Relacionamentos
    comentarios = db.relationship(
        'Comentario',
        backref='post',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='Comentario.data_comentario.desc()'
    )
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref='posts',
        lazy=True)

    def __init__(
            self, titulo, conteudo, categoria, autor_id, media_estrelas=0,
            num_votos=0, data_publicacao=None, ultima_atualizacao=None,
            foto_cover=DEFAULT_COVER_PATH):
        self.titulo = titulo
        self.conteudo = conteudo
        self.categoria = categoria
        self.foto_cover = foto_cover
        self.media_estrelas = media_estrelas
        self.num_votos = num_votos
        self.data_publicacao = data_publicacao if data_publicacao \
            else datetime.now(timezone.utc)
        self.ultima_atualizacao = ultima_atualizacao
        self.autor_id = autor_id

    def __repr__(self) -> str:
        return f"Post({self.id=}, {self.titulo=}, {self.autor_id=})"

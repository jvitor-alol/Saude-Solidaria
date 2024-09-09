from datetime import datetime, timezone

from flask_login import UserMixin

from .relacionamentos import avaliacoes, favoritos, ler_mais_tarde
from .relacionamentos import reports_posts, reports_comentarios
from ..extensions import db

AVATAR_IMG_PATH = '/static/images/default_avatar.png'
PAIS_DEFAULT = 'BR'


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    nome_usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefone = db.Column(db.String(20), unique=True)
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    pais = db.Column(db.String(100), default=PAIS_DEFAULT)
    data_nascimento = db.Column(db.Date)
    genero = db.Column(db.String(20))
    foto_perfil = db.Column(
        db.Text,
        nullable=False,
        default=AVATAR_IMG_PATH)
    bio = db.Column(db.Text)
    data_registro = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultimo_login = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(20), default='ativo')
    notificacoes = db.Column(db.Boolean, default=False)
    tipo_usuario = db.Column(  # 'admin', 'comum' ou 'medico'
        db.String(20),
        default='comum',
        nullable=False)

    # Relacionamentos
    posts = db.relationship(
        'Post', backref='autor', lazy=True, cascade='all, delete-orphan')
    comentarios = db.relationship(
        'Comentario', backref='autor', lazy=True, cascade='all, delete-orphan')
    posts_avaliados = db.relationship(
        'Post',
        secondary=avaliacoes,
        backref='avaliado_por',
        lazy=True)
    posts_favoritados = db.relationship(
        'Post',
        secondary=favoritos,
        backref='favoritado_por',
        lazy=True)
    posts_ler_mais_tarde = db.relationship(
        'Post',
        secondary=ler_mais_tarde,
        backref='ler_mais_tarde_por',
        lazy=True)
    posts_reportados = db.relationship(
        'Post',
        secondary=reports_posts,
        backref='reportado_por',
        lazy=True)
    comentarios_reportados = db.relationship(
        'Comentario',
        secondary=reports_comentarios,
        backref='reportado_por',
        lazy=True)

    def __init__(
            self, nome, sobrenome, nome_usuario, senha, email,
            telefone=None, cidade=None, estado=None, pais=PAIS_DEFAULT,
            data_nascimento=None, genero=None, foto_perfil=AVATAR_IMG_PATH,
            bio=None, data_registro=None, ultimo_login=None, status='ativo',
            notificacoes=False, tipo_usuario='comum'):
        self.nome = nome
        self.sobrenome = sobrenome
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.email = email
        self.telefone = telefone
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.foto_perfil = foto_perfil
        self.bio = bio
        self.data_registro = data_registro if data_registro \
            else datetime.now(timezone.utc)
        self.ultimo_login = ultimo_login
        self.status = status
        self.notificacoes = notificacoes
        self.tipo_usuario = tipo_usuario

    def __repr__(self) -> str:
        return f"Usuario({self.id=}, {self.nome_usuario=}, {self.email=})"

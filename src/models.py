import os
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AVATAR_IMG_PATH = os.path.join(BASE_DIR, 'static/images/default_avatar.png')

# Tabelas associativas (many-to-many)
favoritos = db.Table(
    'favoritos',
    db.Column(
        'usuario_id',
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True),
    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True),
    db.Column(
        'data_adicao',
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False)
)

ler_mais_tarde = db.Table(
    'ler_mais_tarde',
    db.Column(
        'usuario_id',
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True),
    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True),
    db.Column(
        'data_adicao',
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False)
)

avaliacoes = db.Table(
    'avaliacoes',
    db.Column(
        'usuario_id',
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True),
    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True),
    db.Column('estrelas', db.SmallInteger, nullable=False),
    db.Column(
        'data_adicao',
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False)
)

posts_tags = db.Table(
    'posts_tags',
    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True),
    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True)
)

reports_posts = db.Table(
    'reports_posts',
    db.Column(
        'usuario_id',
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True),
    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True),
    db.Column('motivo', db.Text, nullable=False),
    db.Column('descricao', db.Text),
    db.Column(
        'data_report',
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False)
)

reports_comentarios = db.Table(
    'reports_comentarios',
    db.Column(
        'usuario_id',
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True),
    db.Column(
        'comentario_id',
        db.Integer,
        db.ForeignKey('comentarios.id'),
        primary_key=True),
    db.Column('motivo', db.Text, nullable=False),
    db.Column('descricao', db.Text),
    db.Column(
        'data_report',
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), nullable=False)
)


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    nome_usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    pais = db.Column(db.String(100), default='Brasil')
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
    posts = db.relationship('Post', backref='autor', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor', lazy=True)
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
            telefone=None, cidade=None, estado=None, pais='Brasil',
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
        self.data_registro = data_registro if data_registro else datetime.now(
            timezone.utc)
        self.ultimo_login = ultimo_login
        self.status = status
        self.notificacoes = notificacoes
        self.tipo_usuario = tipo_usuario

    def __repr__(self) -> str:
        return f"Usuario({self.id=}, {self.nome_usuario=}, {self.email=})"


class Medico(db.Model):
    __tablename__ = 'medicos'

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True)
    crm = db.Column(db.String(50), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)

    # Relacionamentos
    usuario = db.relationship(
        'Usuario',
        backref=db.backref('medico', uselist=False))

    def __init__(self, usuario_id, crm, especialidade):
        self.usuario_id = usuario_id
        self.crm = crm
        self.especialidade = especialidade

    def __repr__(self) -> str:
        return f"Medico({self.usuario_id=}, {self.crm=})"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
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
    comentarios = db.relationship('Comentario', backref='post', lazy=True)
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref='posts',
        lazy=True)

    def __init__(
            self, titulo, conteudo, categoria, autor_id, media_estrelas=0,
            num_votos=0, data_publicacao=None, ultima_atualizacao=None):
        self.titulo = titulo
        self.conteudo = conteudo
        self.categoria = categoria
        self.media_estrelas = media_estrelas
        self.num_votos = num_votos
        self.data_publicacao = data_publicacao if data_publicacao \
            else datetime.now(timezone.utc)
        self.ultima_atualizacao = ultima_atualizacao
        self.autor_id = autor_id

    def __repr__(self) -> str:
        return f"Post({self.id=}, {self.titulo=}, {self.autor_id=})"


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


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self) -> str:
        return f"Tag({self.id=}, {self.nome=})"

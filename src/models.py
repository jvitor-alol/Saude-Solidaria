import os
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


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
        default=os.path.join(BASE_DIR, 'static/images/default_avatar.png'))
    bio = db.Column(db.Text)
    data_registro = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultimo_login = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(20), default='ativo')
    notificacoes = db.Column(db.Boolean, default=True)
    tipo_usuario = db.Column(  # 'admin', 'comum' ou 'medico'
        db.String(20),
        default='comum',
        nullable=False)

    posts = db.relationship(
        'Post',
        backref='autor_post',
        lazy=True)
    comentarios = db.relationship(
        'Comentario',
        backref='autor_comentario',
        lazy=True)
    favoritos = db.relationship(
        'Favorito',
        backref='usuario_favorito',
        lazy=True)
    ler_mais_tarde = db.relationship(
        'LerMaisTarde',
        backref='usuario_ler_mais_tarde',
        lazy=True)
    posts_avaliados = db.relationship(
        'UsuarioPostNota',
        backref='usuario_avaliador',
        lazy=True)
    posts_reportados = db.relationship(
        'PostReport',
        backref='usuario_post_reportado',
        lazy=True)
    comentarios_reportados = db.relationship(
        'ComentarioReport',
        backref='usuario_comentario_reportado',
        lazy=True)

    def __repr__(self) -> str:
        return f"Usuario('{self.id=}', {self.nome_usuario=}', '{self.email=}')"


class Medico(db.Model):
    __tablename__ = 'medicos'

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        primary_key=True)
    crm = db.Column(db.String(50), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('medico', uselist=False))

    def __repr__(self) -> str:
        return f"Medico('{self.usuario_id=}', '{self.crm=}')"


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

    autor = db.relationship(
        'Usuario',
        backref=db.backref('postagens', lazy=True))
    comentarios = db.relationship(
        'Comentario',
        backref='post_comentario',
        lazy=True)
    notas = db.relationship(
        'UsuarioPostNota',
        backref='post_avaliado',
        lazy=True)
    listado_em_favoritos = db.relationship(
        'Favorito',
        backref='post_favorito',
        lazy=True)
    listado_em_ler_mais_tarde = db.relationship(
        'LerMaisTarde',
        backref='post_ler_mais_tarde',
        lazy=True)
    reports = db.relationship(
        'PostReport',
        backref='post_reportado',
        lazy=True)

    def __repr__(self) -> str:
        return f"Post('{self.id=}', '{self.titulo=}', '{self.autor_id=}')"


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
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=False)

    autor = db.relationship(
        'Usuario',
        backref=db.backref('comentarios_usuario', lazy=True))
    post = db.relationship(
        'Post',
        backref=db.backref('comentarios_post', lazy=True))
    reports = db.relationship(
        'ComentarioReport',
        backref='comentario_reportado',
        lazy=True)

    def __repr__(self) -> str:
        return (f"Comentario('{self.id=}', '{self.autor_id=}', "
                f"'{self.post_id=}')")


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=False)
    data_adicao = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('favoritos_usuario', lazy=True))
    post = db.relationship(
        'Post',
        backref=db.backref('favoritos_post', lazy=True))

    def __repr__(self) -> str:
        return (f"Favorito('{self.id=}', '{self.usuario_id=}', "
                f"'{self.post_id=}')")


class LerMaisTarde(db.Model):
    __tablename__ = 'ler_mais_tarde'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=False)
    data_adicao = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('ler_mais_tarde_usuario', lazy=True))
    post = db.relationship(
        'Post',
        backref=db.backref('ler_mais_tarde_post', lazy=True))

    def __repr__(self) -> str:
        return (f"LerMaisTarde('{self.id=}', '{self.usuario_id=}', "
                f"'{self.post_id=}')")


class PostReport(db.Model):
    __tablename__ = 'post_reports'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    data_report = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('usuario_posts_reportados', lazy=True))
    post = db.relationship(
        'Post',
        backref=db.backref('reports_post', lazy=True))

    def __repr__(self) -> str:
        return (f"PostReport('{self.id=}', '{self.usuario_id=}', "
                f"'{self.post_id=}', '{self.motivo=}')")


class ComentarioReport(db.Model):
    __tablename__ = 'comentario_reports'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    comentario_id = db.Column(
        db.Integer,
        db.ForeignKey('comentarios.id'),
        nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    data_report = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('usuario_comentarios_reportados', lazy=True))
    commentario = db.relationship(
        'Comentario',
        backref=db.backref('reports_comentario', lazy=True))

    def __repr__(self) -> str:
        return (f"ComentarioReport('{self.id=}', '{self.usuario_id=}', "
                f"'{self.comentario_id=}', '{self.motivo=}')")


class UsuarioPostNota(db.Model):
    __tablename__ = 'usuario_post_nota'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    estrelas = db.Column(db.SmallInteger, nullable=False)

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('notas_usuario', lazy=True))
    post = db.relationship(
        'Post',
        backref=db.backref('notas_post', lazy=True))

    def __repr__(self) -> str:
        return (f"UsuarioPostNota('{self.id=}', '{self.usuario_id=}', "
                f"'{self.post_id=}', '{self.estrelas=}')")

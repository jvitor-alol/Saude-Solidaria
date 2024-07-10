import os
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

base_dir = os.path.abspath(os.path.dirname(__file__))


class Usuario(db.Model):
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
        db.Text, nullable=False,
        default=os.path.join(base_dir, 'static/images/default_avatar.png'))
    bio = db.Column(db.Text)
    data_registro = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultimo_login = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(20), default='ativo')
    notificacoes = db.Column(db.Boolean, default=True)
    tipo_usuario = db.Column(
        db.String(20), default='comum', nullable=False)  # 'comum' ou 'medico'

    posts = db.relationship('Post', backref='autor_post', lazy=True)
    comentarios = db.relationship(
        'Comentario', backref='autor_comentario', lazy=True)
    favoritos = db.relationship(
        'Favorito', backref='usuario_favorito', lazy=True)
    ler_mais_tarde = db.relationship(
        'LerMaisTarde', backref='usuario_ler_mais_tarde', lazy=True)
    reports = db.relationship('Report', backref='usuario_report', lazy=True)

    def __repr__(self) -> str:
        return f"User({self.nome_usuario=}, {self.email=})"


class Medico(db.Model):
    __tablename__ = 'medicos'

    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), primary_key=True)
    crm = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)

    usuario = db.relationship(
        'Usuario', backref=db.backref('medico', uselist=False))

    def __repr__(self) -> str:
        return f"Medico({self.usuario_id=}, {self.crm=})"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    estrelas = db.Column(db.SmallInteger, default=0)
    num_votos = db.Column(db.Integer, default=0)
    data_publicacao = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)
    ultima_atualizacao = db.Column(db.DateTime(timezone=True))
    autor_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)

    autor = db.relationship(
        'Usuario', backref=db.backref('postagens', lazy=True))

    def __repr__(self) -> str:
        return f"Post({self.id=}, {self.titulo=}, {self.autor_id=})"


class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    estrelas = db.Column(db.SmallInteger, default=0)
    num_votos = db.Column(db.Integer, default=0)
    data_comentario = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    autor = db.relationship(
        'Usuario', backref=db.backref('comentarios_usuario', lazy=True))
    post = db.relationship(
        'Post', backref=db.backref('comentarios_post', lazy=True))

    def __repr__(self) -> str:
        return f"Comentario({self.id=}, {self.autor_id=}, {self.post_id=})"


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    data_adicao = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario', backref=db.backref('favoritos_usuario', lazy=True))
    post = db.relationship(
        'Post', backref=db.backref('favoritos_post', lazy=True))

    def __repr__(self) -> str:
        return f"Favorito({self.id=}, {self.usuario_id=}, {self.post_id=})"


class LerMaisTarde(db.Model):
    __tablename__ = 'ler_mais_tarde'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    data_adicao = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario', backref=db.backref('ler_mais_tarde_usuario', lazy=True))
    post = db.relationship(
        'Post', backref=db.backref('ler_mais_tarde_post', lazy=True))

    def __repr__(self) -> str:
        return f"LerMaisTarde({self.id=}, {self.usuario_id=}, {self.post_id=})"


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    data_report = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        nullable=False)

    usuario = db.relationship(
        'Usuario', backref=db.backref('reports_usuario', lazy=True))
    post = db.relationship(
        'Post', backref=db.backref('reports_post', lazy=True))

    def __repr__(self) -> str:
        return f"Report({self.id=}, {self.usuario_id=}, {self.post_id=})"

from datetime import datetime, timezone

from .setup import db

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
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
)

from .setup import db, migrate
from .comentario import Comentario
from .usuario import Usuario
from .medico import Medico
from .post import Post
from .tag import Tag


__all__ = [
    'db',
    'migrate',
    'Usuario',
    'Medico',
    'Post',
    'Comentario',
    'Tag',
    'relacionamentos'
]

from ..extensions import db


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

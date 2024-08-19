from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from .helpers import ESPECIALIDADES


class PostForm(FlaskForm):
    titulo = StringField(
        "Titulo", validators=[DataRequired(), Length(min=10, max=255)],
        description="Digite o título da postagem")
    categoria = SelectField(
        "Categoria", validators=[DataRequired()],
        choices=ESPECIALIDADES)
    conteudo = CKEditorField(
        "Conteúdo", validators=[DataRequired()],
        description="Insira o texto aqui...")
    submit = SubmitField("Enviar")

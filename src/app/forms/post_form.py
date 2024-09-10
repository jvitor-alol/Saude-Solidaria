from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SelectField, SubmitField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Optional

from .helpers import ESPECIALIDADES


class PostForm(FlaskForm):
    titulo = StringField(
        "Titulo", validators=[DataRequired(), Length(max=255)],
        description="Digite o título da postagem")
    categoria = SelectField(
        "Categoria", validators=[DataRequired()],
        choices=ESPECIALIDADES)
    foto_cover = FileField(
        "Imagem de capa",
        validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    conteudo = CKEditorField(
        "Conteúdo", validators=[DataRequired()],
        description="Insira o texto aqui...")
    submit = SubmitField("Enviar")

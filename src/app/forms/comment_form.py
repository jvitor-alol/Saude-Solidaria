from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    conteudo = TextAreaField(
        "Adicione um comentário",
        validators=[DataRequired(), Length(max=5000)],
        render_kw={"placeholder": "Seu comentário aqui..."})
    submit = SubmitField("Enviar")

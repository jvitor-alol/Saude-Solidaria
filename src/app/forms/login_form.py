from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField(
        "Senha", validators=[DataRequired(), Length(max=128)])
    lembre_de_mim = BooleanField("Mantenha-me conectado")
    submit = SubmitField("Login")

import pycountry

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms import DateField, TelField, TextAreaField
from wtforms.validators import Length, Email, Optional, ValidationError
from flask_login import current_user

from ..models import Usuario


class UpdateAccountForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[Length(max=255)])
    sobrenome = StringField(
        "Sobrenome", validators=[Length(max=255)])
    nome_usuario = StringField(
        "Nome de usuário", validators=[Length(min=4, max=100)])
    email = StringField(
        "Email", validators=[Email(), Length(max=255)])
    telefone = TelField(
        "Telefone", validators=[Length(min=10, max=15)])
    cidade = StringField("Cidade", validators=[Length(max=100)])
    estado = StringField("Estado", validators=[Length(max=100)])
    pais = SelectField(
        "País",
        choices=[
            (country.alpha_2, country.name) for country in pycountry.countries
        ])
    data_nascimento = DateField("Data de nascimento")
    genero = SelectField(
        "Gênero",
        choices=[
            ("", "Selecione..."),  # Valor vazio para placeholder
            ("masculino", "Masculino"),
            ("feminino", "Feminino"),
            ("outro", "Outro"),
            ("n/a", "Prefiro não informar")
        ],
        default="")
    bio = TextAreaField("Bio")
    especialidade = SelectField(  # Para médicos
        "Especialidade", validators=[Optional()],
        choices=[
            ("clinica geral", "Clínica Geral / Medicina Interna"),
            ("pediatria", "Pediatria"),
            ("ginecologia", "Ginecologia"),
            ("ortopedia", "Ortopedia"),
            ("dermatologia", "Dermatologia"),
            ("cardiologia", "Cardiologia"),
            ("neurologia", "Neurologia"),
            ("oftalmologia", "Oftalmologia"),
            ("psiquiatria", "Psiquiatria"),
            ("oncologia", "Oncologia")
        ])
    notificacoes = BooleanField("Deseja receber notificações?")
    submit = SubmitField("Salvar Alterações")

    def validate_email(self, email: StringField) -> None:
        if email.data == current_user.email:
            return
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Esse email já está sendo utilizado.")

    def validate_nome_usuario(self, nome_usuario: StringField) -> None:
        if nome_usuario.data == current_user.nome_usuario:
            return
        user = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
        if user:
            raise ValidationError("Nome de usuário já utilizado.")

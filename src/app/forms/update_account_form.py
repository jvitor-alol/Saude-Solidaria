import re

import pycountry
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms import DateField, TelField, TextAreaField
from wtforms.validators import Length, Email, Optional, DataRequired
from wtforms.validators import ValidationError
from flask_login import current_user

from ..models import Usuario


class UpdateAccountForm(FlaskForm):
    nome = StringField(
        "Nome", validators=[DataRequired(), Length(max=255)])
    sobrenome = StringField(
        "Sobrenome", validators=[DataRequired(), Length(max=255)])
    nome_usuario = StringField(
        "Nome de usuário", validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=255)])
    telefone = TelField(
        "Telefone", validators=[Optional(), Length(min=10, max=20)])
    cidade = StringField("Cidade", validators=[Optional(), Length(max=100)])
    estado = StringField("Estado", validators=[Optional(), Length(max=100)])
    pais = SelectField(
        "País",
        choices=[
            (country.alpha_2, country.name) for country in pycountry.countries
        ])
    data_nascimento = DateField("Data de nascimento", validators=[Optional()])
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
    bio = TextAreaField("Bio", validators=[Optional()])
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
    foto_perfil = FileField(
        "Atualizar foto de perfil",
        validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    notificacoes = BooleanField("Deseja receber notificações?")
    submit = SubmitField("Salvar Alterações")

    def validate_nome_usuario(self, nome_usuario: StringField) -> None:
        if nome_usuario.data == current_user.nome_usuario:
            return
        user = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
        if user:
            raise ValidationError("Nome de usuário já utilizado.")

    def validate_email(self, email: StringField) -> None:
        if email.data == current_user.email:
            return
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Esse email já está sendo utilizado.")

    def validate_telefone(self, telefone: TelField) -> None:
        # pylint: disable=C0415
        from ..controllers.helpers import normalizar_telefone

        telefone_normal = normalizar_telefone(telefone.data)

        # Número válido
        telefone_re = re.compile(r'^\+\d{1,4}\d{10,15}$')
        if not telefone_re.match(telefone_normal):
            raise ValidationError(
                "Número de telefone inválido (exemplo: +55 (11) 99999-9999).")

        if telefone_normal == normalizar_telefone(current_user.telefone):
            return
        # Check de telefone único
        user = Usuario.query.filter_by(telefone=telefone_normal).first()
        if user:
            raise ValidationError("Telefone já está sendo utilizado.")

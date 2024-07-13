from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import RadioField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Optional
from wtforms.validators import ValidationError

from .models import Usuario, Medico


class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    nome_usuario = StringField(
        'Nome de usuário', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField(
        'Email', validators=[DataRequired(), Email()])
    senha = PasswordField(
        'Senha', validators=[DataRequired(), Length(min=8, max=100)])
    confirmar_senha = PasswordField(
        'Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    tipo_usuario = RadioField(
        'Conta', validators=[DataRequired()],
        choices=[('comum', 'Comum'), ('medico', 'Médico')], )
    crm = StringField('CRM', validators=[Optional(), Length(max=50)])
    especialidade = SelectField(
        'Especialidade', validators=[Optional()],
        choices=[
            ('clinica geral', 'Clínica Geral / Medicina Interna'),
            ('pediatria', 'Pediatria'),
            ('ginecologia', 'Ginecologia'),
            ('ortopedia', 'Ortopedia'),
            ('dermatologia', 'Dermatologia'),
            ('cardiologia', 'Cardiologia'),
            ('neurologia', 'Neurologia'),
            ('oftalmologia', 'Oftalmologia'),
            ('psiquiatria', 'Psiquiatria'),
            ('oncologia', 'Oncologia')
        ])
    submit = SubmitField('Registrar')

    def validate_email(self, email: StringField) -> None:
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já existe no sistema.')

    def validate_nome_usuario(self, nome_usuario: StringField) -> None:
        user = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
        if user:
            raise ValidationError(
                'Nome de usuário já utilizado. Por favor, escolha outro.')

    def validate_crm(self, crm: StringField) -> None:
        medico = Medico.query.filter_by(crm=crm.data).first()
        if medico:
            raise ValidationError(
                'CRM já cadastrado no sistema. Verifique seus dados.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembre_de_mim = BooleanField('Mantenha-me conectado')
    submit = SubmitField('Login')

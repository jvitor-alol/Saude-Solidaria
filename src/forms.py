from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import RadioField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Optional


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


class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembre_de_mim = BooleanField('Mantenha-me conectado')
    submit = SubmitField('Login')

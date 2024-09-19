from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class TicketForm(FlaskForm):
    """
    Formulário para a criação e envio de tickets de suporte.
    Este formulário coleta informações como nome, e-mail, setor, 
    categoria do ticket, descrição do problema e número de patrimônio.
    """
    nome = StringField('Qual seu nome?', validators=[DataRequired(), Length(max=255)])
    email = StringField('Qual seu e-mail?', validators=[DataRequired(), Email(), Length(max=255)])
    
    setor = SelectField('Qual seu setor?', choices=[
        ('Recepção', 'Recepção'), 
        ('Comercial', 'Comercial'),
        ('Planejamento', 'Planejamento'), 
        ('Sac-Atendimento', 'Sac-Atendimento'), 
        ('Jurídico', 'Jurídico'), 
        ('Serviços', 'Serviços'), 
        ('Desenvolvimento', 'Desenvolvimento'), 
        ('Operacional', 'Operacional'), 
        ('Recursos Humanos', 'Recursos Humanos'), 
        ('Cobrança', 'Cobrança'), 
        ('Financeiro', 'Financeiro')
    ], validators=[DataRequired()])
    
    categoria = SelectField('Categoria do Ticket:', choices=[
        ('computador', 'Computador'), 
        ('internet', 'Internet'),
        ('pasta-rede', 'Pasta de Rede'), 
        ('telefonia', 'Telefonia'), 
        ('sistema', 'Sistema'), 
        ('novo-colaborador', 'Novo Colaborador'),
        ('retirada-equipamento', 'Retirada de Equipamento'),
        ('troca-estacao-trabalho', 'Troca de Estação de Trabalho'),
        ('outros', 'Outros')
    ], validators=[DataRequired()])
    
    descricao = TextAreaField('Descrição do Problema:', validators=[DataRequired(), Length(max=255)])
    patrimonio = StringField('Patrimônio', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Enviar Ticket')

class LoginForm(FlaskForm):
    """
    Formulário para login de usuários.
    Coleta as credenciais de nome de usuário e senha para login.
    """
    username = StringField('Qual seu Usuário?', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Qual sua senha?', validators=[DataRequired()])
    submit = SubmitField('Entrar')

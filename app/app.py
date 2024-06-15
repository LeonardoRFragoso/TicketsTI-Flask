from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from sqlalchemy import func, and_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import smtplib
import email.message
import humanize
from humanize import i18n
from datetime import datetime 
import pandas as pd
from io import BytesIO
from flask_admin import AdminIndexView

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    setor = db.Column(db.String(255))
    categoria = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    patrimonio = db.Column(db.String(255))
    status = db.Column(db.String(255))
    data_criacao = db.Column(db.TIMESTAMP)
    horario_inicial_atendimento = db.Column(db.TIMESTAMP)
    pausa_horario_atendimento = db.Column(db.TIMESTAMP)
    horario_retomado_atendimento = db.Column(db.TIMESTAMP)
    horario_final_atendimento = db.Column(db.TIMESTAMP)
    sla = db.Column(db.Interval)

    def send_status_update_email(self):
        email_body = f'Sua solicitação para a equipe de T.I foi recebida e/ou atualizada e agora seu status é {self.status}. Qualquer informação ou comunicação necessária para resolução deste ticket pode e deve ser feita a partir desta conversa de email.'
        enviar_email([self.email, 'ti@rwetelemedicina.com.br'], 'Atualização de status do ticket', email_body)

    def update_status(self, new_status):
        now = func.now()
        if new_status in ['em_andamento', 'Em andamento']:
            if self.status in ['aguardando', 'Aguardando Atendimento']:
                self.horario_inicial_atendimento = now
        elif new_status in ['Pendente', 'pendente']:
            if self.status in ['Em andamento', 'em_andamento']:
                self.pausa_horario_atendimento = now
        elif new_status in ['em_andamento', 'Em andamento']:
            if self.status in ['Pendente', 'pendente']:
                if self.horario_retomado_atendimento:
                    self.horario_retomado_atendimento += now - self.pausa_horario_atendimento
                else:
                    self.horario_retomado_atendimento = now - self.pausa_horario_atendimento
                self.pausa_horario_atendimento = None
        self.status = new_status
        db.session.commit()
        if new_status in ['Concluído', 'concluído']:
            self.calculate_sla()
            db.session.commit()
        self.send_status_update_email()

    def calculate_sla(self):
        if self.horario_inicial_atendimento and self.horario_final_atendimento:
            total_atendimento = self.horario_final_atendimento - self.horario_inicial_atendimento
            if self.pausa_horario_atendimento and self.horario_retomado_atendimento:
                total_atendimento -= self.horario_retomado_atendimento - self.pausa_horario_atendimento
            self.sla = total_atendimento
            i18n.activate("pt_BR")
            sla_legivel = humanize.naturaldelta(total_atendimento)
            self.sla_legivel = sla_legivel
            i18n.deactivate()
            db.session.commit()

    def get_ticket_content(self):
        return f"ID: {self.id}\nNome: {self.nome}\nE-mail: {self.email}\nSetor: {self.setor}\nCategoria: {self.categoria}\nDescrição: {self.descricao}\nPatrimônio: {self.patrimonio}\nStatus: {self.status}\nData de Criação: {self.data_criacao}\nHorário Inicial do Atendimento: {self.horario_inicial_atendimento}\nPausa Horário do Atendimento: {self.pausa_horario_atendimento}\nSLA Retomado: {self.horario_retomado_atendimento}\nSLA Total: {self.sla}"

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id)) if user_id is not None else None

class TicketForm(FlaskForm):
    nome = StringField('Qual seu nome?', validators=[DataRequired()])
    email = StringField('Qual seu e-mail?', validators=[DataRequired(), Email()])
    setor = SelectField('Qual seu setor?', choices=[
        ('', 'Escolha um setor'), ('Recepção', 'Recepção'), ('Comercial', 'Comercial'), 
        ('Planejamento', 'Planejamento'), ('Sac-Atendimento', 'Sac/Atendimento'), 
        ('Juridico', 'Jurídico'), ('Serviços', 'Serviços'), ('Desenvolvimento', 'Desenvolvimento'), 
        ('Operacional', 'Operacional'), ('Rercursos-Humanos', 'Recursos Humanos'), 
        ('Cobrança', 'Cobrança'), ('Financeiro', 'Financeiro')
    ], validators=[DataRequired()])
    categoria = SelectField('Categoria do Ticket:', choices=[
        ('', 'Escolha uma categoria'), ('computador', 'Computador'), ('internet', 'Internet'), 
        ('pasta-rede', 'Pasta de Rede'), ('telefonia', 'Telefonia'), 
        ('sistema', 'Sistema'), ('novo-colaborador', 'Novo Colaborador'), 
        ('retirada-equipamento', 'Retirada de Equipamento'), ('troca-estacao-trabalho', 'Troca de Estação de Trabalho'), 
        ('outros', 'Outros')
    ], validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Problema:', validators=[DataRequired()])
    patrimonio = StringField('Patrimônio', validators=[DataRequired()])
    submit = SubmitField('Enviar Ticket')

class LoginForm(FlaskForm):
    username = StringField('Qual seu Usuário?', validators=[DataRequired()])
    password = PasswordField('Qual sua senha?', validators=[DataRequired()])
    submit = SubmitField('Entrar')

@app.route('/')
def index():
    form = TicketForm()
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.index' if user.is_admin else 'index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = TicketForm()
    if form.validate_on_submit():
        data_criacao = datetime.now()
        ticket = Tickets(
            nome=form.nome.data,
            email=form.email.data,
            setor=form.setor.data,
            categoria=form.categoria.data,
            descricao=form.descricao.data,
            patrimonio=form.patrimonio.data,
            status='Aguardando atendimento',
            data_criacao=data_criacao,
            horario_inicial_atendimento=None,
            pausa_horario_atendimento=None,
            horario_retomado_atendimento=None,
            horario_final_atendimento=None,
            sla=None
        )
        db.session.add(ticket)
        db.session.commit()
        ticket.send_status_update_email()
        flash('Ticket enviado com sucesso!', 'success')
        return redirect(url_for('obg'))
    return render_template('submit.html', form=form)

@app.route('/obg')
def obg():
    return render_template('obg.html')

def enviar_email(destinatarios, assunto, corpo_email):
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'ti@rwetelemedicina.com.br'
    msg['To'] = ", ".join(destinatarios)
    password = 'korkffjuyqewkskc'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    try:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], destinatarios, msg.as_string().encode('utf-8'))
        print('Email enviado')
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

class TicketModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        super(TicketModelView, self).on_model_change(form, model, is_created)
        db.session.flush()
        model.send_status_update_email()
        new_status = form.status.data
        model.update_status(new_status)
        return super(TicketModelView, self).on_model_change(form, model, is_created)

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class CustomAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

admin = Admin(app, template_mode='bootstrap3', index_view=CustomAdminIndexView())
admin.add_view(TicketModelView(Tickets, db.session, name='Lista de Tickets'))

@app.before_request
def check_admin():
    if '/admin' in request.path and not current_user.is_authenticated:
        return redirect(url_for('login'))

class ReportModelView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/report.html')

    @expose('/generate_report', methods=['POST', 'GET'])
    def generate_report_view(self):
        if request.method == 'POST':
            filters = {key: request.form.get(key) for key in request.form}
            report_data = self.generate_report(**filters)

            xlsx_data = BytesIO()
            report_data.to_excel(xlsx_data, index=False, sheet_name='Relatório de Tickets')
            xlsx_data.seek(0)
            response = make_response(xlsx_data.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=Relatorio_de_tickets.xlsx"
            response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        else:
            return self.render('admin/report.html', filters=None)

    def generate_report(self, start_date, end_date, status, nome, email, setor, patrimonio):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query_filters = [
                (Tickets.horario_inicial_atendimento >= start_date) | (Tickets.horario_final_atendimento >= start_date),
                (Tickets.horario_inicial_atendimento <= end_date) | (Tickets.horario_final_atendimento <= end_date)
            ]
            if status:
                query_filters.append(Tickets.status == status)
            if nome:
                query_filters.append(Tickets.nome == nome)
            if email:
                query_filters.append(Tickets.email == email)
            if setor:
                query_filters.append(Tickets.setor == setor)
            if patrimonio:
                query_filters.append(Tickets.patrimonio == patrimonio)
            relevant_tickets = Tickets.query.filter(and_(*query_filters)).all()
            data_list = []
            for ticket in relevant_tickets:
                ticket.calculate_sla()
                data_list.append({
                    'ID': ticket.id,
                    'Nome': ticket.nome,
                    'Email': ticket.email,
                    'Setor': ticket.setor,
                    'Categoria': ticket.categoria,
                    'Descrição': ticket.descricao,
                    'Patrimônio': ticket.patrimonio,
                    'Status': ticket.status,
                    'Data de Criação': ticket.data_criacao,
                    'Horário Inicial Atendimento': ticket.horario_inicial_atendimento,
                    'Pausa Horário Atendimento': ticket.pausa_horario_atendimento,
                    'Retomado Horário Atendimento': ticket.horario_retomado_atendimento,
                    'Horário Final Atendimento': ticket.horario_final_atendimento,
                    'SLA': getattr(ticket, 'sla_legivel', '')
                })
            report_data = pd.DataFrame(data_list)
            return report_data
        except Exception as e:
            print(f"An error occurred in generate_report: {str(e)}")
            raise

admin.add_view(ReportModelView(name='Relatório', endpoint='report_generate_report_view'))

@app.route('/update_ticket_status', methods=['POST'])
def update_ticket_status():
    ticket_id = request.form.get('ticket_id')
    new_status = request.form.get('new_status')
    ticket = db.session.query(Tickets).get(ticket_id)
    if ticket:
        ticket.update_status(new_status)
        content = ticket.get_ticket_content()
        return jsonify({'success': True, 'content': content})
    else:
        return jsonify({'success': False, 'error': 'Ticket not found'})

@app.route('/get_ticket_content', methods=['POST'])
def get_ticket_content():
    ticket_id = request.form.get('ticket_id')
    ticket = Tickets.query.get(ticket_id)
    if ticket:
        content = ticket.get_ticket_content()
        return jsonify({'success': True, 'content': content})
    else:
        return jsonify({'success': False, 'error': 'Ticket not found'})

@app.route('/load_tickets')
def load_tickets():
    all_tickets = Tickets.query.all()
    tickets_data = [{
        'id': ticket.id,
        'nome': ticket.nome,
        'descricao': ticket.descricao,
        'status': ticket.status
    } for ticket in all_tickets]
    return jsonify({'success': True, 'tickets': tickets_data})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8005)

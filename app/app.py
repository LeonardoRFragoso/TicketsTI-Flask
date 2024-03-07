from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from sqlalchemy import func
import smtplib
import email.message
import humanize
from humanize import i18n
from datetime import datetime, timedelta
from sqlalchemy import text


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Definição do modelo de usuário
class User(db.Model, UserMixin):
    __tablename__ = 'User' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

# Definição do modelo de ticket
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    setor = db.Column(db.String(255))
    categoria = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    patrimonio = db.Column(db.String(255))
    status = db.Column(db.String(255))
    teamviewer = db.Column(db.String(255))
    horario_inicial_atendimento = db.Column(db.TIMESTAMP)
    pausa_horario_atendimento = db.Column(db.TIMESTAMP)
    horario_retomado_atendimento = db.Column(db.TIMESTAMP)
    horario_final_atendimento = db.Column(db.TIMESTAMP)
    sla = db.Column(db.Interval)

    # Função para enviar e-mail de atualização de status
    def send_status_update_email(self):
        email_body = f'O status do seu ticket (ID: {self.id}) agora é {self.status}.'
        enviar_email([self.email, 'ti@rwetelemedicina.com.br'], 'Atualização de status do ticket', email_body)

    # Função para atualizar o status do ticket e SLA
    def update_status(self, new_status):
        now = func.now()
        if new_status in ['em_andamento', 'Em andamento', 'em andamento']:
            if self.status in ['Aguardando atendimento', 'aguardando']:
                self.horario_inicial_atendimento = now

        elif new_status in ['Pendente', 'pendente']:
            if self.status in ['Em andamento', 'em andamento', 'em_andamento']:
                self.pausa_horario_atendimento = now

        elif new_status in ['em_andamento', 'Em andamento', 'em andamento']:
            if self.status in ['Pendente', 'pendente']:
                if self.horario_retomado_atendimento:
                    self.horario_retomado_atendimento += now - self.pausa_horario_atendimento
                else:
                    self.horario_retomado_atendimento = now - self.pausa_horario_atendimento
                self.pausa_horario_atendimento = None  # Limpe o campo de pausa

        self.status = new_status
        db.session.commit()  # Garanta o commit antes de potencialmente modificar o SLA
        
        # Verifique se o novo status é 'Concluído' ou 'Finalizado' para calcular o SLA
        if new_status in ['Concluído', 'Finalizado']:
            self.calculate_sla()
            db.session.commit()  # Faça commit das alterações após calcular o SLA

        self.send_status_update_email()


    # Função para calcular o SLA
    def calculate_sla(self):
        if self.horario_inicial_atendimento and self.horario_final_atendimento:
            total_atendimento = self.horario_final_atendimento - self.horario_inicial_atendimento
            if self.pausa_horario_atendimento and self.horario_retomado_atendimento:
                total_atendimento -= self.horario_retomado_atendimento - self.pausa_horario_atendimento

            # Atualize o campo SLA com a diferença calculada
            self.sla = total_atendimento

            # Ative a localização para pt_BR
            i18n.activate("pt_BR")

            # Converta a diferença para um formato mais legível (dias, horas, minutos)
            sla_legivel = humanize.naturaldelta(total_atendimento)

            # Salve o valor legível em português brasileiro
            self.sla_legivel = sla_legivel
            i18n.deactivate()
            db.session.commit() 

            # Converta a diferença para um formato mais legível (dias, horas, minutos)

    def get_ticket_content(self):
        # Retorna todas as informações do ticket
        return f"ID: {self.id}\nNome: {self.nome}\nE-mail: {self.email}\nSetor: {self.setor}\nCategoria: {self.categoria}\nDescrição: {self.descricao}\nPatrimônio: {self.patrimonio}\nStatus: {self.status}\nTeamviewer: {self.teamviewer}\nHorário Inicial do Atendimento: {self.horario_inicial_atendimento}\nPausa Horário do Atendimento: {self.pausa_horario_atendimento}\nSLA Retomado: {self.tempo_retomado_atendimento}\nSLA Total: {self.tempo_total_atendimento}\nTempo Total: {self.tempo_total}"

# Configuração do carregamento de usuário para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

# Configuração do painel de administração
admin = Admin(app, template_mode='bootstrap3')

# Definição da visualização do modelo Ticket no painel de administração
class TicketModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        super(TicketModelView, self).on_model_change(form, model, is_created)
        if not is_created:
            db.session.flush()
            model.send_status_update_email()

            new_status = form.status.data
            model.update_status(new_status)
                

        return super(TicketModelView, self).on_model_change(form, model, is_created)

# Adição da visualização do modelo Ticket ao painel de administração
ticket_model_view = TicketModelView(Ticket, db.session, name='Lista de Tickets')
admin.add_view(ticket_model_view)

# Definição da visualização do modelo User no painel de administração
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

# Middleware para verificar autenticação antes de acessar a página de administração
@app.before_request
def check_admin():
    if '/admin' in request.path and not current_user.is_authenticated:
        return redirect(url_for('login'))

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            return redirect(url_for('admin.index' if user.is_admin else 'index'))
    return render_template('login.html')

# Rota para realizar o logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rota para submissão do formulário de criação de ticket
@app.route('/submit', methods=['POST'])
def submit():
    ticket = Ticket(
        nome=request.form.get('nome'),
        email=request.form.get('email'),
        setor=request.form.get('setor'),
        categoria=request.form.get('categoria'),
        descricao=request.form.get('descricao'),
        patrimonio=request.form.get('patrimonio'),
        status='Aguardando atendimento',
        teamviewer=request.form.get('teamviewer'),
        horario_inicial_atendimento=None,
        pausa_horario_atendimento=None,
        horario_retomado_atendimento=None,
        horario_final_atendimento=None,
        sla=None
    )
    db.session.add(ticket)
    db.session.commit()
    ticket.send_status_update_email()
    return redirect(url_for('obg'))

# Função para enviar e-mails
def enviar_email(destinatarios, assunto, corpo_email):
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'leonardorfragoso@gmail.com'
    msg['To'] = ", ".join(destinatarios)
    password = 'aurtmmbtztvuuhea'
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

# Rota para a página de agradecimento
@app.route('/obg')
def obg():
    return render_template('obg.html')

# Rota para atualizar o status do ticket via AJAX
@app.route('/update_ticket_status', methods=['POST'])

def update_ticket_status():
    ticket_id = request.form.get('ticket_id')
    new_status = request.form.get('new_status')
    ticket = db.session.query(Ticket).get(ticket_id)
    
    if ticket:
        ticket.update_status(new_status)
        content = ticket.get_ticket_content()
        return jsonify({'success': True, 'content': content})
    else:
        return jsonify({'success': False, 'error': 'Ticket not found'})

# Rota para obter o conteúdo do ticket via AJAX
@app.route('/get_ticket_content', methods=['POST'])
def get_ticket_content():
    ticket_id = request.form.get('ticket_id')

    # Recupere o ticket do banco de dados usando o ticket_id
    ticket = Ticket.query.get(ticket_id)

    if ticket:
        content = ticket.get_ticket_content()
        return jsonify({'success': True, 'content': content})
    else:
        return jsonify({'success': False, 'error': 'Ticket not found'})

# Rota para carregar os tickets
@app.route('/load_tickets')
def load_tickets():
    all_tickets = Ticket.query.all()
    tickets_data = [{
        'id': ticket.id,
        'nome': ticket.nome,
        'descricao': ticket.descricao,
        'status': ticket.status
    } for ticket in all_tickets]
    return jsonify({'success': True, 'tickets': tickets_data})

# Execução do aplicativo em modo de depuração
if __name__ == "__main__":
    app.run(debug=True)

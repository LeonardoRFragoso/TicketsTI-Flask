from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from datetime import datetime, timedelta
import humanize
from humanize import i18n
from app import db
from app.utils import enviar_email

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
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

    def __repr__(self):
        return f"<User {self.username}>"


class Tickets(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    setor = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    patrimonio = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='Aguardando atendimento', nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    horario_inicial_atendimento = db.Column(db.TIMESTAMP)
    pausa_horario_atendimento = db.Column(db.TIMESTAMP)
    horario_retomado_atendimento = db.Column(db.TIMESTAMP)
    horario_final_atendimento = db.Column(db.TIMESTAMP)
    sla = db.Column(db.Interval)

    def send_status_update_email(self):
        """
        Envia um e-mail para o usuário informando sobre a mudança de status do ticket.
        """
        email_body = f"""
        Sua solicitação foi recebida/atualizada e o status atual do ticket é {self.status}.
        Qualquer informação adicional será comunicada via este e-mail.
        """
        try:
            enviar_email([self.email, 'ti@empresa.com'], 'Atualização de Status do Ticket', email_body)
        except Exception as e:
            # Tratar o erro de envio de e-mail
            print(f"Erro ao enviar e-mail de atualização de status: {e}")

    def update_status(self, new_status):
        """
        Atualiza o status do ticket e os horários de atendimento.
        """
        now = datetime.now()
        if new_status in ['Em andamento', 'em_andamento']:
            if self.status in ['Aguardando atendimento', 'aguardando']:
                self.horario_inicial_atendimento = now
        elif new_status in ['Pendente', 'pendente']:
            if self.status in ['Em andamento', 'em_andamento']:
                self.pausa_horario_atendimento = now
        elif new_status in ['Em andamento', 'em_andamento']:
            if self.status in ['Pendente', 'pendente']:
                if self.horario_retomado_atendimento:
                    self.horario_retomado_atendimento += now - self.pausa_horario_atendimento
                else:
                    self.horario_retomado_atendimento = now - self.pausa_horario_atendimento
                self.pausa_horario_atendimento = None
        elif new_status in ['Concluído', 'concluído']:
            self.horario_final_atendimento = now
            self.calculate_sla()
        
        self.status = new_status
        db.session.commit()
        self.send_status_update_email()

    def calculate_sla(self):
        """
        Calcula o SLA (Service Level Agreement) para o ticket com base nos horários de atendimento.
        """
        if not self.horario_inicial_atendimento or not self.horario_final_atendimento:
            return

        total_atendimento = self.horario_final_atendimento - self.horario_inicial_atendimento
        if self.pausa_horario_atendimento and self.horario_retomado_atendimento:
            total_atendimento -= self.horario_retomado_atendimento - self.pausa_horario_atendimento
        self.sla = total_atendimento

        # Converter SLA para um formato legível
        i18n.activate("pt_BR")
        sla_legivel = humanize.naturaldelta(total_atendimento)
        self.sla_legivel = sla_legivel
        i18n.deactivate()
        db.session.commit()

    def __repr__(self):
        return f"<Ticket {self.id} - {self.status}>"

from app import db
from datetime import datetime
import humanize
from humanize import i18n

class Tickets(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    setor = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    patrimonio = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), default='Aguardando atendimento')
    data_criacao = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    horario_inicial_atendimento = db.Column(db.TIMESTAMP, nullable=True)
    pausa_horario_atendimento = db.Column(db.TIMESTAMP, nullable=True)
    horario_retomado_atendimento = db.Column(db.TIMESTAMP, nullable=True)
    horario_final_atendimento = db.Column(db.TIMESTAMP, nullable=True)
    sla = db.Column(db.Interval, nullable=True)

    def update_status(self, new_status):
        """Atualiza o status do ticket e ajusta os horários de atendimento."""
        now = datetime.now()
        if new_status.lower() == 'em andamento':
            if self.status.lower() == 'aguardando atendimento':
                self.horario_inicial_atendimento = now
            elif self.status.lower() == 'pendente':
                self.horario_retomado_atendimento = now - self.pausa_horario_atendimento
                self.pausa_horario_atendimento = None
        elif new_status.lower() == 'pendente':
            if self.status.lower() == 'em andamento':
                self.pausa_horario_atendimento = now
        elif new_status.lower() in ['concluído', 'concluido']:
            self.horario_final_atendimento = now
            self.calculate_sla()

        self.status = new_status
        db.session.commit()

    def calculate_sla(self):
        """Calcula o tempo total de atendimento (SLA)"""
        if self.horario_inicial_atendimento and self.horario_final_atendimento:
            total_atendimento = self.horario_final_atendimento - self.horario_inicial_atendimento
            if self.pausa_horario_atendimento and self.horario_retomado_atendimento:
                total_atendimento -= self.horario_retomado_atendimento - self.pausa_horario_atendimento
            self.sla = total_atendimento
            i18n.activate("pt_BR")
            self.sla_legivel = humanize.naturaldelta(total_atendimento)
            i18n.deactivate()
            db.session.commit()

    def __repr__(self):
        return f'<Ticket {self.id}: {self.nome}, Status: {self.status}>'

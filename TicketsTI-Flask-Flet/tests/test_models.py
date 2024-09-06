from app.models.user import User
from app.models.ticket import Tickets
from datetime import datetime, timedelta
import pytest

def test_password_hashing():
    user = User(username='testuser')
    user.set_password('testpassword')
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')

def test_ticket_creation():
    ticket = Tickets(
        nome='Leonardo Fragoso',
        email='leonardo@example.com',
        setor='Suporte',
        categoria='Software',
        descricao='Problema com o sistema',
        patrimonio='PC-1234',
        status='Aguardando atendimento',
        data_criacao=datetime.utcnow()
    )
    assert ticket.nome == 'Leonardo Fragoso'
    assert ticket.email == 'leonardo@example.com'
    assert ticket.status == 'Aguardando atendimento'

def test_sla_calculation():
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(hours=2)
    ticket = Tickets(
        horario_inicial_atendimento=start_time,
        horario_final_atendimento=end_time
    )
    ticket.calculate_sla()
    assert ticket.sla == timedelta(hours=2)

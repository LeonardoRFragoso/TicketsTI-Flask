from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.models.user import User
from app.models.ticket import Tickets
from app import db
from datetime import datetime

api = Blueprint('api', __name__)

# Rota para login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'success': True, 'message': 'Login successful', 'is_admin': user.is_admin})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# Rota para logout
@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout successful'})

# Rota para criar um ticket
@api.route('/tickets', methods=['POST'])
@login_required
def create_ticket():
    data = request.get_json()
    
    new_ticket = Tickets(
        nome=data.get('nome'),
        email=data.get('email'),
        setor=data.get('setor'),
        categoria=data.get('categoria'),
        descricao=data.get('descricao'),
        patrimonio=data.get('patrimonio'),
        status='Aguardando atendimento',
        data_criacao=datetime.now()
    )
    
    db.session.add(new_ticket)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ticket created successfully', 'ticket_id': new_ticket.id})

# Rota para listar todos os tickets (pode ser usado pela tela de administração)
@api.route('/tickets', methods=['GET'])
@login_required
def get_tickets():
    tickets = Tickets.query.all()
    tickets_list = [
        {
            'id': ticket.id,
            'nome': ticket.nome,
            'email': ticket.email,
            'setor': ticket.setor,
            'categoria': ticket.categoria,
            'descricao': ticket.descricao,
            'patrimonio': ticket.patrimonio,
            'status': ticket.status,
            'data_criacao': ticket.data_criacao,
        }
        for ticket in tickets
    ]
    return jsonify({'success': True, 'tickets': tickets_list})

# Rota para atualizar o status de um ticket
@api.route('/tickets/<int:ticket_id>', methods=['PUT'])
@login_required
def update_ticket_status(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    if not ticket:
        return jsonify({'success': False, 'message': 'Ticket not found'}), 404

    data = request.get_json()
    new_status = data.get('status')
    ticket.update_status(new_status)

    return jsonify({'success': True, 'message': 'Ticket status updated', 'new_status': new_status})

# Rota para visualizar um ticket específico
@api.route('/tickets/<int:ticket_id>', methods=['GET'])
@login_required
def get_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    if not ticket:
        return jsonify({'success': False, 'message': 'Ticket not found'}), 404

    ticket_data = {
        'id': ticket.id,
        'nome': ticket.nome,
        'email': ticket.email,
        'setor': ticket.setor,
        'categoria': ticket.categoria,
        'descricao': ticket.descricao,
        'patrimonio': ticket.patrimonio,
        'status': ticket.status,
        'data_criacao': ticket.data_criacao,
        'horario_inicial_atendimento': ticket.horario_inicial_atendimento,
        'pausa_horario_atendimento': ticket.pausa_horario_atendimento,
        'horario_retomado_atendimento': ticket.horario_retomado_atendimento,
        'horario_final_atendimento': ticket.horario_final_atendimento,
        'sla': ticket.sla_legivel if hasattr(ticket, 'sla_legivel') else None
    }
    
    return jsonify({'success': True, 'ticket': ticket_data})

# Rota para deletar um ticket
@api.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ticket_id):
    ticket = Tickets.query.get(ticket_id)
    if not ticket:
        return jsonify({'success': False, 'message': 'Ticket not found'}), 404

    db.session.delete(ticket)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ticket deleted successfully'})

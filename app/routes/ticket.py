from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import Tickets
from app import db
from datetime import datetime

# Criação do blueprint para lidar com tickets
ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/submit', methods=['POST'])
def submit_ticket():
    """
    Rota para criar e salvar um novo ticket de suporte.
    Recebe uma requisição POST com os dados do ticket em formato JSON.
    """
    try:
        # Recebe os dados enviados no corpo da requisição (em formato JSON)
        data = request.get_json()

        # Extrai os dados do JSON
        nome = data.get('nome')
        email = data.get('email')
        setor = data.get('setor')
        categoria = data.get('categoria')
        descricao = data.get('descricao')
        patrimonio = data.get('patrimonio')

        # Verifica se todos os campos obrigatórios foram fornecidos
        if not nome or not email or not setor or not categoria or not descricao or not patrimonio:
            return jsonify({"success": False, "message": "Todos os campos são obrigatórios."}), 400

        # Cria um novo ticket no banco de dados
        novo_ticket = Tickets(
            nome=nome,
            email=email,
            setor=setor,
            categoria=categoria,
            descricao=descricao,
            patrimonio=patrimonio,
            data_criacao=datetime.utcnow(),
            status='Aguardando atendimento'
        )

        # Adiciona e comita o novo ticket ao banco de dados
        db.session.add(novo_ticket)
        db.session.commit()

        # Retorna uma resposta de sucesso
        return jsonify({"success": True, "message": "Ticket enviado com sucesso!"}), 200

    except Exception as e:
        # Retorna uma resposta de erro em caso de falha
        return jsonify({"success": False, "error": str(e)}), 500

@ticket_bp.route('/tickets', methods=['GET'])
@login_required
def listar_tickets():
    """
    Rota para listar todos os tickets do sistema.
    Retorna os tickets no formato JSON.
    Acesso restrito a usuários autenticados.
    """
    try:
        # Obtém todos os tickets do banco de dados
        tickets = Tickets.query.all()

        # Formata os tickets para JSON
        tickets_json = []
        for ticket in tickets:
            tickets_json.append({
                'id': ticket.id,
                'nome': ticket.nome,
                'email': ticket.email,
                'setor': ticket.setor,
                'categoria': ticket.categoria,
                'descricao': ticket.descricao,
                'patrimonio': ticket.patrimonio,
                'status': ticket.status,
                'data_criacao': ticket.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                'horario_inicial_atendimento': ticket.horario_inicial_atendimento.strftime('%Y-%m-%d %H:%M:%S') if ticket.horario_inicial_atendimento else None,
                'horario_final_atendimento': ticket.horario_final_atendimento.strftime('%Y-%m-%d %H:%M:%S') if ticket.horario_final_atendimento else None
            })

        return jsonify({"success": True, "tickets": tickets_json}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

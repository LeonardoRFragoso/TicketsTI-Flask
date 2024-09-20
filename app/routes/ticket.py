from flask import Blueprint, request, jsonify
from app.models import Tickets
from app import db
from datetime import datetime
import logging

# Criação do blueprint para lidar com tickets
ticket_bp = Blueprint('ticket', __name__)

# Configuração de logs para monitorar as ações
logging.basicConfig(level=logging.INFO)

@ticket_bp.route('/submit', methods=['POST'])
def submit_ticket():
    """
    Rota para criar e salvar um novo ticket de suporte.
    Recebe uma requisição POST com os dados do ticket em formato JSON.
    """
    try:
        data = request.get_json()

        if not data:
            logging.error("Nenhum dado foi enviado na solicitação.")
            return jsonify({"success": False, "message": "Nenhum dado foi enviado."}), 400

        nome = data.get('nome')
        email = data.get('email')
        setor = data.get('setor')
        categoria = data.get('categoria')
        descricao = data.get('descricao')
        patrimonio = data.get('patrimonio')

        # Verifica se todos os campos obrigatórios foram fornecidos
        if not all([nome, email, setor, categoria, descricao, patrimonio]):
            logging.error("Campos obrigatórios não foram preenchidos corretamente.")
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

        logging.info(f"Novo ticket criado por {nome} (ID: {novo_ticket.id})")

        return jsonify({"success": True, "message": "Ticket enviado com sucesso!"}), 200

    except Exception as e:
        logging.error(f"Erro ao enviar ticket: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@ticket_bp.route('/tickets', methods=['GET'])
def listar_tickets():
    """
    Rota para listar todos os tickets do sistema.
    Retorna os tickets no formato JSON.
    """
    try:
        tickets = Tickets.query.all()
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

        logging.info(f"{len(tickets_json)} tickets listados.")
        return jsonify({"success": True, "tickets": tickets_json}), 200

    except Exception as e:
        logging.error(f"Erro ao listar tickets: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@ticket_bp.route('/update_status/<int:ticket_id>', methods=['PUT'])
def update_status(ticket_id):
    """
    Rota para atualizar o status de um ticket.
    Recebe o ID do ticket e o novo status via PUT request.
    """
    try:
        data = request.get_json()
        new_status = data.get('status')

        if not new_status:
            logging.error("Nenhum status fornecido para o ticket.")
            return jsonify({"success": False, "message": "Nenhum status fornecido."}), 400

        # Verifica se o ticket existe
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            logging.error(f"Ticket com ID {ticket_id} não encontrado.")
            return jsonify({"success": False, "message": "Ticket não encontrado."}), 404

        # Verifica se o status é válido
        valid_status = ['Aguardando atendimento', 'Em andamento', 'Concluído', 'Pendente']
        if new_status not in valid_status:
            logging.error(f"Status '{new_status}' inválido.")
            return jsonify({"success": False, "message": "Status inválido."}), 400

        # Atualiza o status e os horários conforme necessário
        ticket.status = new_status
        if new_status == 'Em andamento' and not ticket.horario_inicial_atendimento:
            ticket.horario_inicial_atendimento = datetime.utcnow()
        elif new_status == 'Concluído' and not ticket.horario_final_atendimento:
            ticket.horario_final_atendimento = datetime.utcnow()

        db.session.commit()

        logging.info(f"Status do ticket {ticket_id} atualizado para '{new_status}'")
        return jsonify({"success": True, "message": "Status atualizado com sucesso!"}), 200

    except Exception as e:
        logging.error(f"Erro ao atualizar status do ticket {ticket_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

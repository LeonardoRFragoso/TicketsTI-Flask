from flask import Blueprint, request, make_response, jsonify
import pandas as pd
from io import BytesIO
from datetime import datetime
from app.models import Tickets
from app import db
from sqlalchemy import and_

# Criação do blueprint de relatórios
report_bp = Blueprint('report', __name__)

@report_bp.route('/generate_report', methods=['POST'])
def generate_report_view():
    """
    Rota para gerar relatórios de tickets com base em filtros fornecidos via requisição POST.
    Retorna um arquivo Excel com os tickets filtrados.
    """
    try:
        # Recebendo os filtros enviados pelo frontend (ex: Streamlit)
        filters = request.get_json()

        # Extraindo os filtros recebidos
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        status = filters.get('status')
        nome = filters.get('nome')
        email = filters.get('email')
        setor = filters.get('setor')
        patrimonio = filters.get('patrimonio')

        # Convertendo as datas recebidas do JSON para o formato datetime
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Criando a lista de filtros para consulta no banco de dados
        query_filters = []
        if start_date:
            query_filters.append((Tickets.horario_inicial_atendimento >= start_date) | (Tickets.horario_final_atendimento >= start_date))
        if end_date:
            query_filters.append((Tickets.horario_inicial_atendimento <= end_date) | (Tickets.horario_final_atendimento <= end_date))
        if status:
            query_filters.append(Tickets.status == status)
        if nome:
            query_filters.append(Tickets.nome.ilike(f"%{nome}%"))
        if email:
            query_filters.append(Tickets.email.ilike(f"%{email}%"))
        if setor:
            query_filters.append(Tickets.setor == setor)
        if patrimonio:
            query_filters.append(Tickets.patrimonio.ilike(f"%{patrimonio}%"))

        # Realizando a consulta no banco de dados com os filtros aplicados
        relevant_tickets = Tickets.query.filter(and_(*query_filters)).all()

        # Criando a lista de dicionários com os dados relevantes dos tickets
        data_list = []
        for ticket in relevant_tickets:
            # Calcula o SLA para o ticket
            ticket.calculate_sla()

            # Adiciona o ticket à lista de resultados
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
                'Horário Final Atendimento': ticket.horario_final_atendimento,
                'SLA': getattr(ticket, 'sla_legivel', '')
            })

        # Convertendo a lista de dicionários para um DataFrame do Pandas
        report_data = pd.DataFrame(data_list)

        # Convertendo o DataFrame para um arquivo Excel em memória
        output = BytesIO()
        report_data.to_excel(output, index=False, sheet_name="Relatório de Tickets")
        output.seek(0)

        # Gerando a resposta com o arquivo Excel para download
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=Relatorio_de_tickets.xlsx"
        response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        return response
    
    except Exception as e:
        # Retorna um erro caso algo dê errado durante a geração do relatório
        return jsonify({"success": False, "error": str(e)}), 500
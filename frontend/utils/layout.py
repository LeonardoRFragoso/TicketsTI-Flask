import streamlit as st
from frontend.utils.api_request import atualizar_status  # Função para atualizar status via API
from datetime import datetime

# Função para ordenar os tickets por data de criação
def ordenar_por_data(tickets):
    return sorted(tickets, key=lambda x: datetime.strptime(x['data_criacao'], '%Y-%m-%d %H:%M:%S'), reverse=True)

# Função para exibir os tickets organizados em colunas e com funcionalidade de arrastar e soltar
def mostrar_tickets_em_colunas(tickets):
    # Estilos para os cards e colunas
    card_style = """
    <style>
    .card {
        background-color: #333;
        color: white;
        padding: 20px;
        margin: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    }
    .card h4 {
        margin: 0;
        padding-bottom: 10px;
        font-size: 18px;
    }
    .card p {
        margin: 5px 0;
    }
    .column-header {
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
        text-align: center;
        color: white;
    }
    .ticket-column {
        min-height: 400px;
        padding: 10px;
        background-color: #222;
        border-radius: 10px;
        border: 2px dashed #444;
    }
    .empty-column {
        display: none;
    }
    </style>
    <script>
    function allowDrop(ev) {
      ev.preventDefault();
    }

    function drag(ev) {
      ev.dataTransfer.setData("text", ev.target.id);
    }

    async function drop(ev, status) {
      ev.preventDefault();
      var data = ev.dataTransfer.getData("text");
      var ticketElement = document.getElementById(data);
      document.getElementById(status).appendChild(ticketElement);

      // Pegando o ID do ticket a partir do elemento arrastado
      var ticketId = data.split("_")[1];

      // Fazendo a chamada para o backend para atualizar o status no banco de dados
      const response = await fetch(`/update_status/` + ticketId, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: status })
      });

      if (!response.ok) {
        alert("Erro ao atualizar o status no servidor.");
        // Caso a atualização falhe, move o ticket de volta ao seu status original
        document.getElementById(ticketElement.dataset.status).appendChild(ticketElement);
      } else {
        // Atualizando o status no frontend após mover
        ticketElement.dataset.status = status;
      }
    }
    </script>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    # Organizando os tickets por status e data
    tickets_aguardando = ordenar_por_data([t for t in tickets if t['status'] == 'Aguardando atendimento'])
    tickets_andamento = ordenar_por_data([t for t in tickets if t['status'] == 'Em andamento'])
    tickets_concluido = ordenar_por_data([t for t in tickets if t['status'] == 'Concluído'])
    tickets_pendente = ordenar_por_data([t for t in tickets if t['status'] == 'Pendente'])

    # Criando colunas para cada status de ticket
    col1, col2, col3, col4 = st.columns(4)

    # Coluna Aguardando Atendimento
    with col1:
        st.markdown("<div class='column-header'>Aguardando Atendimento</div>", unsafe_allow_html=True)
        if tickets_aguardando:
            st.markdown("<div id='Aguardando atendimento' class='ticket-column' ondrop='drop(event, \"Aguardando atendimento\")' ondragover='allowDrop(event)'>", unsafe_allow_html=True)
            for ticket in tickets_aguardando:
                st.markdown(f"""
                <div id="ticket_{ticket['id']}" class='card' draggable='true' ondragstart='drag(event)' data-status='Aguardando atendimento'>
                    <h4>{ticket['categoria']}</h4>
                    <p><b>ID:</b> {ticket['id']}</p>
                    <p><b>Nome:</b> {ticket['nome']}</p>
                    <p><b>E-mail:</b> {ticket['email']}</p>
                    <p><b>Setor:</b> {ticket['setor']}</p>
                    <p><b>Status:</b> {ticket['status']}</p>
                    <p><b>Data de Criação:</b> {ticket['data_criacao']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='empty-column'></div>", unsafe_allow_html=True)

    # Coluna Em Andamento
    with col2:
        st.markdown("<div class='column-header'>Em Andamento</div>", unsafe_allow_html=True)
        if tickets_andamento:
            st.markdown("<div id='Em andamento' class='ticket-column' ondrop='drop(event, \"Em andamento\")' ondragover='allowDrop(event)'>", unsafe_allow_html=True)
            for ticket in tickets_andamento:
                st.markdown(f"""
                <div id="ticket_{ticket['id']}" class='card' draggable='true' ondragstart='drag(event)' data-status='Em andamento'>
                    <h4>{ticket['categoria']}</h4>
                    <p><b>ID:</b> {ticket['id']}</p>
                    <p><b>Nome:</b> {ticket['nome']}</p>
                    <p><b>E-mail:</b> {ticket['email']}</p>
                    <p><b>Setor:</b> {ticket['setor']}</p>
                    <p><b>Status:</b> {ticket['status']}</p>
                    <p><b>Data de Criação:</b> {ticket['data_criacao']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='empty-column'></div>", unsafe_allow_html=True)

    # Coluna Pendente
    with col3:
        st.markdown("<div class='column-header'>Pendente</div>", unsafe_allow_html=True)
        if tickets_pendente:
            st.markdown("<div id='Pendente' class='ticket-column' ondrop='drop(event, \"Pendente\")' ondragover='allowDrop(event)'>", unsafe_allow_html=True)
            for ticket in tickets_pendente:
                st.markdown(f"""
                <div id="ticket_{ticket['id']}" class='card' draggable='true' ondragstart='drag(event)' data-status='Pendente'>
                    <h4>{ticket['categoria']}</h4>
                    <p><b>ID:</b> {ticket['id']}</p>
                    <p><b>Nome:</b> {ticket['nome']}</p>
                    <p><b>E-mail:</b> {ticket['email']}</p>
                    <p><b>Setor:</b> {ticket['setor']}</p>
                    <p><b>Status:</b> {ticket['status']}</p>
                    <p><b>Data de Criação:</b> {ticket['data_criacao']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='empty-column'></div>", unsafe_allow_html=True)

    # Coluna Concluído
    with col4:
        st.markdown("<div class='column-header'>Concluído</div>", unsafe_allow_html=True)
        if tickets_concluido:
            st.markdown("<div id='Concluído' class='ticket-column' ondrop='drop(event, \"Concluído\")' ondragover='allowDrop(event)'>", unsafe_allow_html=True)
            for ticket in tickets_concluido:
                st.markdown(f"""
                <div id="ticket_{ticket['id']}" class='card' draggable='true' ondragstart='drag(event)' data-status='Concluído'>
                    <h4>{ticket['categoria']}</h4>
                    <p><b>ID:</b> {ticket['id']}</p>
                    <p><b>Nome:</b> {ticket['nome']}</p>
                    <p><b>E-mail:</b> {ticket['email']}</p>
                    <p><b>Setor:</b> {ticket['setor']}</p>
                    <p><b>Status:</b> {ticket['status']}</p>
                    <p><b>Data de Criação:</b> {ticket['data_criacao']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='empty-column'></div>", unsafe_allow_html=True)

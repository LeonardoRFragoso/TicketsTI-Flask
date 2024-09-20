import streamlit as st
from frontend.utils.api_request import listar_tickets  # Certifique-se que api_request está correto
from frontend.utils.layout import mostrar_tickets_em_colunas  # Importa a função correta

def mostrar_tela():
    """
    Função para exibir a tela de listagem de tickets.
    """
    st.subheader("Tickets Registrados")
    
    # Obter os tickets do backend
    tickets = listar_tickets()
    
    # Exibir os tickets em colunas de acordo com o status
    if tickets:
        mostrar_tickets_em_colunas(tickets)  # Chama a função correta para exibir os tickets em colunas
    else:
        st.info("Nenhum ticket registrado.")

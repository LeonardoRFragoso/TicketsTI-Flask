import streamlit as st
from frontend.utils.api_request import gerar_relatorio  # Corrigido o import para a função correta

def mostrar_tela():
    st.subheader("Gerar Relatório de Tickets")
    
    # Formulário para selecionar filtros do relatório
    start_date = st.date_input("Data inicial")
    end_date = st.date_input("Data final")
    status = st.selectbox("Status", ["", "Aguardando", "Em andamento", "Concluído", "Pendente"])
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    setor = st.text_input("Setor")
    patrimonio = st.text_input("Patrimônio")

    # Botão para gerar o relatório
    if st.button("Gerar Relatório"):
        # Chama a função gerar_relatorio para enviar os filtros ao backend
        gerar_relatorio(start_date, end_date, status, nome, email, setor, patrimonio)

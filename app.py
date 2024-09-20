import streamlit as st
from frontend.utils.enviar_ticket import mostrar_tela as tela_enviar_ticket
from frontend.utils.listar_ticket import mostrar_tela as tela_listar_tickets
from frontend.utils.login import mostrar_tela as tela_login
from frontend.utils.logout import mostrar_tela as tela_logout
from frontend.utils.gerar_relatorio import mostrar_tela as tela_gerar_relatorio

# Inicializa o estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Define o menu na barra lateral
if st.session_state.logged_in:
    menu = st.sidebar.radio("Menu", ["Enviar Ticket", "Listar Tickets", "Gerar Relatório", "Logout"])
else:
    menu = st.sidebar.radio("Menu", ["Enviar Ticket", "Login"])

# Exibe a tela apropriada com base no menu selecionado
if menu == "Enviar Ticket":
    tela_enviar_ticket()
elif menu == "Login":
    tela_login()
elif menu == "Listar Tickets" and st.session_state.logged_in:
    tela_listar_tickets()
elif menu == "Gerar Relatório" and st.session_state.logged_in:
    tela_gerar_relatorio()
elif menu == "Logout" and st.session_state.logged_in:
    tela_logout()
else:
    st.warning("Você precisa estar logado para acessar essa seção.")

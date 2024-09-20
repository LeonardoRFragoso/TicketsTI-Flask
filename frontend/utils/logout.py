import streamlit as st
from frontend.utils.api_request import logout_user  # Certifique-se que api_request está correto

def mostrar_tela():
    """
    Função que exibe a tela de logout e realiza o logout do usuário.
    """
    # Botão de logout
    if st.button("Logout"):
        # Chama a função logout_user para encerrar a sessão do usuário
        logout_user()
        st.success("Logout realizado com sucesso!")

import streamlit as st
from frontend.utils.api_request import login_user

def mostrar_tela():
    st.subheader("Login no Sistema")
    
    # Formulário de login
    with st.form(key="login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        login_button = st.form_submit_button(label="Login")

    if login_button:
        if username and password:
            # Chama a função login_user para autenticar
            if login_user(username, password):
                # Redireciona para a tela de listagem de tickets após login
                st.experimental_rerun()
        else:
            st.error("Por favor, preencha o nome de usuário e a senha.")

import streamlit as st
from frontend.utils.api_request import login_user

def mostrar_tela():
    st.subheader("Login no Sistema")

    # Verificar se já está logado
    if st.session_state.get("logged_in", False):
        st.info("Você já está logado.")
        return

    # Formulário de login
    with st.form(key="login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button(label="Login")

    if login_button:
        if username and password:
            if login_user(username, password):
                st.success("Login realizado com sucesso!")
                st.session_state.logged_in = True
                # Não fazemos mais o redirecionamento, apenas atualizamos a sessão
            else:
                st.error("Falha no login. Verifique suas credenciais.")
        else:
            st.error("Por favor, preencha o nome de usuário e a senha.")

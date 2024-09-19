import streamlit as st
import requests
from datetime import datetime
from io import BytesIO

# URL do backend Flask
BASE_URL = "http://localhost:8005"

# Função para enviar o ticket para o backend do Flask
def enviar_ticket(nome, email, setor, categoria, descricao, patrimonio):
    try:
        # Enviando os dados do formulário para o backend do Flask
        response = requests.post(f"{BASE_URL}/submit", json={
            'nome': nome,
            'email': email,
            'setor': setor,
            'categoria': categoria,
            'descricao': descricao,
            'patrimonio': patrimonio
        })
        
        # Tratamento de resposta da API
        if response.status_code == 200:
            st.success("Ticket enviado com sucesso!")
        elif response.status_code == 400:
            erro = response.json().get('message', 'Erro desconhecido.')
            st.error(f"Erro ao enviar o ticket: {erro}")
        else:
            st.error(f"Erro ao enviar o ticket. Código de resposta: {response.status_code}")
    
    except Exception as e:
        st.error(f"Erro ao tentar enviar o ticket: {e}")

# Função para login no sistema
def login_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                st.success("Login realizado com sucesso!")
                return True
            else:
                st.error(result.get('message', 'Erro desconhecido.'))
                return False
        elif response.status_code == 400:
            erro = response.json().get('message', 'Erro desconhecido.')
            st.error(f"Erro no login: {erro}")
            return False
        else:
            st.error(f"Erro no login. Código de resposta: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Erro ao tentar logar: {e}")
        return False

# Função para logout no sistema
def logout_user():
    try:
        response = requests.post(f"{BASE_URL}/logout")
        if response.status_code == 200:
            st.success("Logout realizado com sucesso!")
        else:
            st.error(f"Erro ao realizar logout. Código de resposta: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao tentar deslogar: {e}")

# Função para listar todos os tickets do usuário logado
def listar_tickets():
    try:
        response = requests.get(f"{BASE_URL}/tickets")
        if response.status_code == 200:
            tickets = response.json().get("tickets", [])
            if tickets:
                st.subheader("Tickets Registrados")
                for ticket in tickets:
                    st.write(f"ID: {ticket['id']}")
                    st.write(f"Nome: {ticket['nome']}")
                    st.write(f"E-mail: {ticket['email']}")
                    st.write(f"Setor: {ticket['setor']}")
                    st.write(f"Categoria: {ticket['categoria']}")
                    st.write(f"Descrição: {ticket['descricao']}")
                    st.write(f"Patrimônio: {ticket['patrimonio']}")
                    st.write(f"Status: {ticket['status']}")
                    st.write(f"Data de Criação: {ticket['data_criacao']}")
                    st.write(f"Horário Inicial Atendimento: {ticket['horario_inicial_atendimento']}")
                    st.write(f"Horário Final Atendimento: {ticket['horario_final_atendimento']}")
                    st.markdown("---")
            else:
                st.info("Nenhum ticket registrado.")
        else:
            st.error(f"Erro ao listar os tickets. Código de resposta: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao tentar listar os tickets: {e}")

# Função para gerar relatórios
def gerar_relatorio(start_date, end_date, status, nome, email, setor, patrimonio):
    filters = {
        "start_date": start_date.strftime('%Y-%m-%d') if start_date else None,
        "end_date": end_date.strftime('%Y-%m-%d') if end_date else None,
        "status": status,
        "nome": nome,
        "email": email,
        "setor": setor,
        "patrimonio": patrimonio
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate_report", json=filters)
        
        if response.status_code == 200:
            output = BytesIO(response.content)
            st.download_button(
                label="Baixar Relatório",
                data=output,
                file_name="Relatorio_de_tickets.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            erro = response.json().get('error', 'Erro desconhecido.')
            st.error(f"Erro ao gerar o relatório: {erro}")
    except Exception as e:
        st.error(f"Erro ao tentar gerar o relatório: {e}")

# Cabeçalho da página
st.title("Sistema de Tickets - Suporte TI")

# Opções de navegação
menu = ["Enviar Ticket", "Login", "Logout", "Listar Tickets", "Gerar Relatório"]
escolha = st.sidebar.selectbox("Menu", menu)

# Formulário de envio de ticket
if escolha == "Enviar Ticket":
    st.subheader("Preencha o formulário abaixo para enviar um ticket de suporte.")
    
    with st.form(key="ticket_form"):
        nome = st.text_input("Qual seu nome?", max_chars=255)
        email = st.text_input("Qual seu e-mail?", max_chars=255)
        setor = st.selectbox("Qual seu setor?", [
            "Recepção", "Comercial", "Planejamento", "Sac-Atendimento", "Jurídico", 
            "Serviços", "Desenvolvimento", "Operacional", "Recursos Humanos", 
            "Cobrança", "Financeiro"
        ])
        categoria = st.selectbox("Categoria do Ticket:", [
            "Computador", "Internet", "Pasta de Rede", "Telefonia", "Sistema", 
            "Novo Colaborador", "Retirada de Equipamento", "Troca de Estação de Trabalho", 
            "Outros"
        ])
        descricao = st.text_area("Descrição do Problema:", max_chars=255)
        patrimonio = st.text_input("Patrimônio", max_chars=255)

        submit_button = st.form_submit_button(label="Enviar Ticket")

    if submit_button:
        if not nome or not email or not setor or not categoria or not descricao or not patrimonio:
            st.error("Por favor, preencha todos os campos corretamente.")
        else:
            enviar_ticket(nome, email, setor, categoria, descricao, patrimonio)

# Tela de Login
elif escolha == "Login":
    st.subheader("Login no Sistema")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if username and password:
            if login_user(username, password):
                st.success("Bem-vindo!")
                listar_tickets()  # Lista os tickets após o login
        else:
            st.error("Por favor, preencha o nome de usuário e senha.")

# Tela de Logout
elif escolha == "Logout":
    if st.button("Logout"):
        logout_user()

# Tela de Listagem de Tickets
elif escolha == "Listar Tickets":
    listar_tickets()

# Tela de geração de relatório
elif escolha == "Gerar Relatório":
    st.subheader("Gerar Relatório de Tickets")
    start_date = st.date_input("Data inicial")
    end_date = st.date_input("Data final")
    status = st.selectbox("Status", ["", "Aguardando", "Em andamento", "Concluído", "Pendente"])
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    setor = st.text_input("Setor")
    patrimonio = st.text_input("Patrimônio")

    if st.button("Gerar Relatório"):
        gerar_relatorio(start_date, end_date, status, nome, email, setor, patrimonio)

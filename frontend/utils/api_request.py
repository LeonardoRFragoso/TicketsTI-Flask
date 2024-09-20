import streamlit as st
import requests
from io import BytesIO

# Base URL da API Flask
BASE_URL = "http://localhost:8005"

# Função para enviar um ticket ao backend
def enviar_ticket(nome, email, setor, categoria, descricao, patrimonio):
    try:
        response = requests.post(f"{BASE_URL}/submit", json={
            'nome': nome,
            'email': email,
            'setor': setor,
            'categoria': categoria,
            'descricao': descricao,
            'patrimonio': patrimonio
        })
        if response.status_code == 200:
            st.success("Ticket enviado com sucesso!")
        else:
            erro = response.json().get('message', 'Erro desconhecido.')
            st.error(f"Erro ao enviar o ticket: {erro}")
    except Exception as e:
        st.error(f"Erro ao tentar enviar o ticket: {e}")

# Função para listar os tickets do backend
def listar_tickets():
    try:
        # Verifica se há cookie de sessão armazenado
        cookies = {'session': st.session_state.get('session_cookie')}
        response = requests.get(f"{BASE_URL}/tickets", cookies=cookies)
        if response.status_code == 200:
            return response.json().get("tickets", [])
        else:
            st.error(f"Erro ao listar os tickets: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Erro ao tentar listar os tickets: {e}")
        return []

# Função para fazer login
def login_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/login", json={'username': username, 'password': password})
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                st.session_state['logged_in'] = True
                st.session_state['session_cookie'] = response.cookies.get('session')
                st.success("Login realizado com sucesso!")
                return True
            else:
                st.error(result.get('message', 'Erro desconhecido.'))
                return False
        else:
            st.error(f"Erro no login. Código de resposta: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Erro ao tentar logar: {e}")
        return False

# Função para fazer logout
def logout_user():
    try:
        cookies = {'session': st.session_state.get('session_cookie')}
        response = requests.post(f"{BASE_URL}/logout", cookies=cookies)
        if response.status_code == 200:
            st.session_state['logged_in'] = False
            st.session_state['session_cookie'] = None
            st.success("Logout realizado com sucesso!")
        else:
            st.error(f"Erro ao realizar logout. Código de resposta: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao tentar deslogar: {e}")

# Função para gerar relatório de tickets
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
        cookies = {'session': st.session_state.get('session_cookie')}
        response = requests.post(f"{BASE_URL}/generate_report", json=filters, cookies=cookies)
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

# Função para atualizar o status do ticket
def atualizar_status(ticket_id, novo_status):
    try:
        cookies = {'session': st.session_state.get('session_cookie')}
        response = requests.put(f"{BASE_URL}/update_status/{ticket_id}", json={'status': novo_status}, cookies=cookies)
        if response.status_code == 200:
            st.success(f"Status do ticket {ticket_id} atualizado para '{novo_status}'!")
        else:
            st.error(f"Erro ao atualizar o status: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao tentar atualizar o status: {e}")

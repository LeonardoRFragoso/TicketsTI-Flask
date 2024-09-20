import streamlit as st
from frontend.utils.api_request import enviar_ticket  # Certifique-se de que api_request está correto

def mostrar_tela():
    st.subheader("Preencha o formulário abaixo para enviar um ticket de suporte.")

    # Verifica se o form_id já existe no estado da sessão e o inicializa se necessário
    if 'form_id' not in st.session_state:
        st.session_state['form_id'] = 0  # Inicializa o form_id na sessão

    # Gerando uma chave única para o formulário
    form_key = f"ticket_form_{st.session_state['form_id']}"

    # Formulário de envio de ticket com chave única
    with st.form(key=form_key):
        nome = st.text_input("Qual seu nome?", max_chars=255)
        email = st.text_input("Qual seu e-mail?", max_chars=255)
        setor = st.selectbox("Qual seu setor?", [
            "Recepção", "Comercial", "Planejamento", "Sac-Atendimento", "Jurídico", 
            "Serviços", "Desenvolvimento", "Operacional", "Recursos Humanos", 
            "Cobrança", "Financeiro"
        ])
        categoria = st.selectbox("Categoria do Ticket:", [
            "Computador", "Internet", "Pasta de Rede", "Telefonia", 
            "Sistema", "Novo Colaborador", "Retirada de Equipamento", 
            "Troca de Estação de Trabalho", "Outros"
        ])
        descricao = st.text_area("Descrição do Problema:", max_chars=255)
        patrimonio = st.text_input("Patrimônio", max_chars=255)
        
        # Botão de submissão
        submit_button = st.form_submit_button(label="Enviar Ticket")

    # Quando o formulário é submetido
    if submit_button:
        # Validação básica
        if not nome or not email or not setor or not categoria or not descricao or not patrimonio:
            st.error("Por favor, preencha todos os campos corretamente.")
        else:
            # Envia o ticket para o backend
            enviar_ticket(nome, email, setor, categoria, descricao, patrimonio)
            st.success("Ticket enviado com sucesso!")

            # Incrementa o form_id para a próxima vez que o formulário for chamado
            st.session_state['form_id'] += 1

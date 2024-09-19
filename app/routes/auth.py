from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app.forms import LoginForm
from app.models import User
import logging

# Instância da proteção CSRF
csrf = CSRFProtect()

# Criação do blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Certifique-se de que o CSRF está corretamente desativado para a rota de login
@csrf.exempt
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota para autenticação de usuários.
    Recebe uma requisição POST com dados em formato JSON.
    Se o login for bem-sucedido, o usuário será autenticado e uma resposta JSON será retornada.
    """
    data = request.get_json()  # Recebe os dados JSON do Streamlit

    if not data:
        logging.error('Nenhum dado foi enviado.')
        return jsonify({'success': False, 'message': 'Nenhum dado foi enviado.'}), 400
    
    logging.info(f"Dados recebidos para login: {data}")  # Log dos dados recebidos
    
    # Criação manual de um formulário para validação de dados
    form = LoginForm(data=data)

    # Verifica se o formulário é válido
    if form.validate():
        # Busca o usuário no banco de dados com base no nome de usuário
        user = User.query.filter_by(username=form.username.data).first()
        
        if user:
            logging.info(f"Usuário encontrado: {user.username}")
        
        # Verifica se o usuário existe e se a senha é válida
        if user and user.verify_password(form.password.data):
            # Faz o login do usuário
            login_user(user)
            logging.info(f"Usuário {user.username} logado com sucesso.")
            
            # Retorna uma resposta JSON indicando sucesso
            return jsonify({'success': True, 'is_admin': user.is_admin})
        else:
            # Mensagem de erro caso as credenciais estejam incorretas
            logging.warning(f"Usuário ou senha inválidos para o usuário: {form.username.data}")
            return jsonify({'success': False, 'message': 'Usuário ou senha inválidos.'}), 401
    else:
        # Se o formulário não for válido, exibe os erros de validação
        logging.error(f"Erros de validação: {form.errors}")
        return jsonify({'success': False, 'message': 'Dados inválidos.', 'errors': form.errors}), 400

@csrf.exempt  # Certifique-se de desativar o CSRF também para logout
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Rota para logout de usuários autenticados.
    Recebe uma requisição POST e, ao realizar o logout, retorna uma resposta JSON indicando sucesso.
    """
    # Faz o logout do usuário autenticado
    logout_user()

    logging.info(f"Usuário fez logout com sucesso.")
    
    # Retorna uma resposta JSON indicando que o logout foi bem-sucedido
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso.'})

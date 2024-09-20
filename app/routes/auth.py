from flask import Blueprint, request, jsonify, redirect, url_for, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app.forms import LoginForm
from app.models import User
import logging

# Instância da proteção CSRF
csrf = CSRFProtect()

# Criação do blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Configuração de logs para monitoramento
logging.basicConfig(level=logging.INFO)

@csrf.exempt
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota de login para usuários. Recebe dados de login (username e password) via POST
    e autentica o usuário se as credenciais forem válidas.
    """
    data = request.get_json()

    if not data:
        logging.error('Nenhum dado foi enviado na solicitação.')
        return jsonify({'success': False, 'message': 'Nenhum dado foi enviado.'}), 400
    
    form = LoginForm(data=data)

    # Valida o formulário de login
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user)
            logging.info(f"Usuário {user.username} logado com sucesso.")
            
            # Cria a resposta com sucesso no login e redirecionamento
            response = make_response(jsonify({
                'success': True,
                'is_admin': user.is_admin,
                'redirect': url_for('ticket.listar_tickets'),
                'message': 'Login realizado com sucesso!'
            }))
            
            # Inclui o cookie de sessão
            session_cookie = request.cookies.get('session')
            if session_cookie:
                response.set_cookie('session', session_cookie, httponly=True)
                logging.info(f"Cookie de sessão definido com sucesso para o usuário {user.username}.")
            else:
                logging.warning("Nenhum cookie de sessão foi encontrado para definir.")
            
            return response
        else:
            logging.warning(f"Falha no login: usuário ou senha inválidos para o usuário: {form.username.data}")
            return jsonify({'success': False, 'message': 'Usuário ou senha inválidos.'}), 401
    else:
        logging.error(f"Erros de validação no formulário: {form.errors}")
        return jsonify({'success': False, 'message': 'Dados inválidos.', 'errors': form.errors}), 400


@csrf.exempt
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Rota para logout de usuários autenticados.
    Recebe uma requisição POST e, ao realizar o logout, retorna uma resposta JSON indicando sucesso.
    """
    # Faz o logout do usuário autenticado
    username = current_user.username if current_user.is_authenticated else 'Desconhecido'
    logout_user()
    logging.info(f"Usuário {username} fez logout com sucesso.")
    
    # Cria a resposta indicando que o logout foi bem-sucedido
    response = jsonify({'success': True, 'message': 'Logout realizado com sucesso.'})
    # Remove o cookie de sessão
    response.delete_cookie('session')
    
    return response


@csrf.exempt
@auth_bp.route('/login', methods=['GET'])
def login_get():
    """
    Rota para redirecionar requisições GET para a página correta em caso de redirecionamento automático.
    """
    logging.info("Tentativa de login usando GET, mas a rota aceita apenas POST.")
    return jsonify({"message": "Utilize uma requisição POST para fazer login."}), 405

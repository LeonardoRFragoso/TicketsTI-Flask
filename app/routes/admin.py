from flask import Blueprint, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import db
from app.models import Tickets, User

# Criação do Blueprint admin
admin_bp = Blueprint('admin', __name__)

class AdminModelView(ModelView):
    def is_accessible(self):
        # Verifica se o usuário está autenticado e é administrador
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redireciona para a página de login se o usuário não tiver acesso
        return redirect(url_for('auth.login'))

class TicketModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        # Quando um ticket é criado ou alterado, o status é atualizado
        super(TicketModelView, self).on_model_change(form, model, is_created)
        db.session.flush()
        
        # Envia o e-mail de atualização de status do ticket
        model.send_status_update_email()
        
        # Atualiza o status do ticket com base no novo valor do formulário
        new_status = form.status.data
        model.update_status(new_status)
        
        return super(TicketModelView, self).on_model_change(form, model, is_created)

# Função para configurar o painel admin
def setup_admin(app):
    admin = Admin(app, template_mode='bootstrap3')
    
    # Adiciona a view do modelo User (para gerenciamento de usuários)
    admin.add_view(AdminModelView(User, db.session))
    
    # Adiciona a view do modelo Tickets (para gerenciamento de tickets)
    admin.add_view(TicketModelView(Tickets, db.session, name='Lista de Tickets'))

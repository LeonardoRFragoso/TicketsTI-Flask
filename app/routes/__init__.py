from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.report import report_bp
from app.routes.ticket import ticket_bp  # Importa o blueprint de ticket

# Função que registra os blueprints na aplicação principal
def register_blueprints(app):
    """
    Função para registrar todos os blueprints da aplicação.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(ticket_bp)  # Registra o blueprint de ticket

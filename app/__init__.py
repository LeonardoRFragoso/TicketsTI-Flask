from flask import Flask, Blueprint  # Certifique-se de importar Blueprint aqui
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

# Inicializa as extensões
db = SQLAlchemy()
login_manager = LoginManager()

# Função para criar a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Carregar as configurações do config.py
    app.config.from_object(Config)

    # Inicializa as extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configuração da página de login
    login_manager.login_view = 'auth.login'

    # Inicializa as migrações do banco de dados
    migrate = Migrate(app, db)

    # Registra os blueprints
    try:
        register_blueprints(app)
    except Exception as e:
        app.logger.error(f"Erro ao registrar blueprints: {e}")
    
    return app

# Função que registra os blueprints na aplicação principal
def register_blueprints(app):
    """
    Função para registrar todos os blueprints da aplicação.
    """
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.report import report_bp
    from app.routes.ticket import ticket_bp  # Certifique-se que este import está correto

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(ticket_bp)  # Certifique-se que este blueprint está registrado

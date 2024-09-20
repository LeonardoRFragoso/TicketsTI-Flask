from flask import Flask
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
    login_manager.login_message = "Você precisa estar logado para acessar esta página."
    login_manager.login_message_category = "info"

    # Inicializa as migrações do banco de dados
    migrate = Migrate(app, db)

    # Registrando os blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.report import report_bp
    from app.routes.ticket import ticket_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(ticket_bp)

    # Adiciona o user_loader ao LoginManager
    from app.models import User  # Agora podemos importar User sem causar ciclo de dependência

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Carrega o usuário a partir do ID

    return app

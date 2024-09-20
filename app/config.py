import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Classe de configuração que carrega as variáveis de ambiente e define as configurações 
    essenciais da aplicação Flask, como o banco de dados, e-mail, e segurança.
    """
    
    # Chave secreta usada para manter os dados das sessões seguras
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave_padrao_mudar_para_producao')

    # URL do banco de dados obtida das variáveis de ambiente
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    
    # Desativa o rastreamento de modificações do SQLAlchemy para melhorar o desempenho
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de e-mail para envio de notificações
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # E-mail do administrador do sistema (para notificações e comunicações críticas)
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@empresa.com')

    # Configurações de segurança adicionais
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ['true', '1', 't']
    REMEMBER_COOKIE_SECURE = os.getenv('REMEMBER_COOKIE_SECURE', 'False').lower() in ['true', '1', 't']
    REMEMBER_COOKIE_HTTPONLY = os.getenv('REMEMBER_COOKIE_HTTPONLY', 'True').lower() in ['true', '1', 't']

    # Definição da página de login
    LOGIN_VIEW = 'auth.login'  # Definindo a view para redirecionamento de login
    
    # Configuração para lembrar sessão do usuário
    REMEMBER_COOKIE_DURATION = int(os.getenv('REMEMBER_COOKIE_DURATION', 3600))  # 1 hora de duração padrão

    # Desativar o CSRF globalmente para simplificar em desenvolvimento
    WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED', 'False').lower() in ['true', '1', 't']

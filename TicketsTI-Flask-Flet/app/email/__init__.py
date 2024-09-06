import smtplib
from flask import current_app

def init_email():
    """
    Inicializa a configuração do sistema de e-mail, extraindo as configurações do arquivo de configuração do Flask.
    """
    smtp_server = current_app.config.get('MAIL_SERVER')
    smtp_port = current_app.config.get('MAIL_PORT')
    smtp_username = current_app.config.get('MAIL_USERNAME')
    smtp_password = current_app.config.get('MAIL_PASSWORD')
    mail_sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    
    return {
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
        'smtp_username': smtp_username,
        'smtp_password': smtp_password,
        'mail_sender': mail_sender
    }

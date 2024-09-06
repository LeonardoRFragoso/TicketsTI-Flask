import smtplib
import email.message
import threading
from flask import current_app
from app.email import init_email

def send_async_email(to, subject, body):
    """
    Função para envio de e-mails de forma assíncrona utilizando threading.
    """
    email_config = init_email()

    def send_email():
        try:
            msg = email.message.Message()
            msg['Subject'] = subject
            msg['From'] = email_config['mail_sender']
            msg['To'] = ", ".join(to)
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(body)

            smtp_server = email_config['smtp_server']
            smtp_port = email_config['smtp_port']
            smtp_username = email_config['smtp_username']
            smtp_password = email_config['smtp_password']

            # Conexão com o servidor SMTP
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Utilizar TLS para segurança
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], to, msg.as_string().encode('utf-8'))
            server.quit()
            
            print("E-mail enviado com sucesso!")
        
        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")
    
    # Executa o envio de e-mail em uma thread separada para não bloquear o sistema
    threading.Thread(target=send_email).start()

from smtplib import SMTP
import email.message
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def enviar_email(destinatarios, assunto, corpo_email):
    """
    Função para enviar um e-mail utilizando o servidor SMTP do Gmail.

    Args:
        destinatarios (list): Lista de endereços de e-mail dos destinatários.
        assunto (str): Assunto do e-mail.
        corpo_email (str): Corpo do e-mail em formato HTML ou texto.

    Returns:
        bool: Retorna True se o e-mail for enviado com sucesso, ou False em caso de erro.
    """
    # Configurações do e-mail
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = os.getenv('EMAIL_SENDER')  # E-mail do remetente (configurado no .env)
    msg['To'] = ", ".join(destinatarios)      # Destinatários como string separada por vírgulas

    # Obtenção da senha do e-mail do remetente a partir das variáveis de ambiente
    password = os.getenv('EMAIL_PASSWORD')
    
    # Configuração do conteúdo do e-mail (HTML ou texto)
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    try:
        # Conexão com o servidor SMTP do Gmail
        server = SMTP('smtp.gmail.com:587')
        server.starttls()  # Inicia a conexão TLS
        server.login(msg['From'], password)  # Autentica no servidor SMTP

        # Enviar o e-mail para os destinatários
        server.sendmail(msg['From'], destinatarios, msg.as_string().encode('utf-8'))
        
        # Fechar a conexão com o servidor SMTP
        server.quit()

        print("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
        return False

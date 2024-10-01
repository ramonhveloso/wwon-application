import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

# Configurações do servidor de e-mail
SMTP_SERVER = os.getenv("SMTP_SERVER")  # Endereço do servidor SMTP
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Porta do servidor SMTP
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Nome de usuário do e-mail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Senha do e-mail

if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD]):
    raise ValueError("As variáveis de ambiente SMTP_SERVER, SMTP_USERNAME e SMTP_PASSWORD devem estar definidas.")

def send_password_reset_email(to_email: str, reset_link: str):
    """Envia um e-mail de redefinição de senha para o usuário."""
    
    # Cria o objeto da mensagem
    msg = MIMEMultipart()
    msg['From'] = str(SMTP_USERNAME)
    msg['To'] = to_email
    msg['Subject'] = "Redefinição de Senha"
    
    # Cria o corpo do e-mail em HTML
    body = f"""
    <html>
        <body>
            <h2>Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Você solicitou a redefinição da sua senha. Clique no botão abaixo para redefini-la:</p>
            <p style="text-align:center;">
                <a href="{reset_link}" style="
                    padding: 10px 20px; 
                    background-color: #007BFF; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px;">
                    Redefinir Senha
                </a>
            </p>
            <p>Se você não solicitou essa alteração, pode ignorar este e-mail.</p>
            <p>Atenciosamente,<br>Sua Equipe</p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Conecta ao servidor SMTP e envia o e-mail
        with smtplib.SMTP(str(SMTP_SERVER), SMTP_PORT) as server:
            server.starttls()  # Ativa a segurança TLS
            server.login(str(SMTP_USERNAME), str(SMTP_PASSWORD))  # Faz login no servidor
            server.send_message(msg)  # Envia a mensagem
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email: " + str(e))

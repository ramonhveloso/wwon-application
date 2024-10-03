import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException

# Configurações do servidor de e-mail
SMTP_SERVER = os.getenv("SMTP_SERVER")  # Endereço do servidor SMTP
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # Porta do servidor SMTP
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Nome de usuário do e-mail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Senha do e-mail

if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD]):
    raise ValueError(
        "As variáveis de ambiente SMTP_SERVER, SMTP_USERNAME e SMTP_PASSWORD devem estar definidas."
    )


async def send_pin_email(to_email: str, pin: str):
    """Envia um e-mail com o PIN de recuperação de senha."""

    # Cria o objeto da mensagem
    msg = MIMEMultipart()
    msg["From"] = str(SMTP_USERNAME)
    msg["To"] = to_email
    msg["Subject"] = "Seu código de recuperação de senha"

    # Template moderno em HTML para o e-mail
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <h2 style="text-align: center; color: #333333;">Código de Recuperação de Senha</h2>
                <p style="font-size: 16px; color: #555555;">Olá,</p>
                <p style="font-size: 16px; color: #555555;">
                    Você solicitou a recuperação da sua senha. Use o código abaixo para redefini-la:
                </p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="
                        display: inline-block;
                        font-size: 22px;
                        color: #ffffff;
                        background-color: #007BFF;
                        padding: 15px 30px;
                        border-radius: 5px;
                        font-weight: bold;
                        letter-spacing: 2px;">
                        {pin}
                    </span>
                </div>
                <p style="font-size: 16px; color: #555555;">
                    Este código é válido por 5 minutos. Se você não solicitou essa alteração, por favor, ignore este e-mail.
                </p>
                <p style="font-size: 16px; color: #555555;">Atenciosamente,<br>wwon applicationgeo</p>
            </div>
        </body>
    </html>
    """

    msg.attach(MIMEText(body, "html"))

    try:
        # Conecta ao servidor SMTP e envia o e-mail
        with smtplib.SMTP_SSL(str(SMTP_SERVER), SMTP_PORT) as server:
            server.login(str(SMTP_USERNAME), str(SMTP_PASSWORD))
            server.send_message(msg, to_addrs=to_email)
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(status_code=400, detail="Invalid email address")
    except smtplib.SMTPException as e:
        raise HTTPException(
            status_code=503, detail="Email service unavailable: " + str(e)
        )

import smtplib
from email.message import EmailMessage
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def send_otp_email(email_to: str, otp_code: str) -> bool:
    """
    Envía un correo con el código OTP de 6 dígitos con diseño HTML profesional.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(f"SMTP no configurado. Código OTP para {email_to}: {otp_code}")
        return False
        
    try:
        msg = EmailMessage()
        msg['Subject'] = f'🔑 Tu Código de Verificación es: {otp_code} - Shopyn Golden Store'
        msg['From'] = f"Shopyn Golden Store <{settings.SMTP_USER}>"
        msg['To'] = email_to
        
        text_content = f"""Hola,

Gracias por registrarte en Shopyn Golden Store.

Tu código de verificación de 6 dígitos es: {otp_code}

Ingresa este código en la aplicación móvil para activar tu cuenta.
Este código caducará en 15 minutos.
"""
        msg.set_content(text_content)

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Código de Verificación</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; padding: 40px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 550px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="background: linear-gradient(135deg, #e11d48 0%, #be123c 100%); padding: 35px 20px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 0.5px;">Shopyn Golden Store</h1>
                            <p style="color: #fecdd3; margin: 6px 0 0 0; font-size: 14px; font-weight: 500;">Verificación de Cuenta de Cliente</p>
                        </td>
                    </tr>

                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 40px 35px; text-align: center;">
                            <h2 style="color: #0f172a; font-size: 22px; margin-top: 0; margin-bottom: 12px; font-weight: 700;">¡Bienvenido a la Boutique!</h2>
                            <p style="color: #475569; font-size: 15px; line-height: 1.6; margin-bottom: 28px;">
                                Para completar tu registro y acceder a nuestro catálogo exclusivo de poleras, ingresa el siguiente código de 6 dígitos en tu aplicación móvil:
                            </p>

                            <!-- OTP Box -->
                            <div style="background-color: #fff1f2; border: 2px dashed #fecdd3; border-radius: 14px; padding: 20px; margin: 20px 0; text-align: center;">
                                <span style="font-family: 'Courier New', Courier, monospace; font-size: 36px; font-weight: 900; letter-spacing: 10px; color: #e11d48;">
                                    {otp_code}
                                </span>
                            </div>

                            <!-- Expiration Warning -->
                            <p style="color: #94a3b8; font-size: 13px; margin-top: 24px;">
                                ⏱️ Este código caducará automáticamente en <strong>15 minutos</strong>.
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="background-color: #f8fafc; padding: 20px; border-top: 1px solid #f1f5f9;">
                            <p style="color: #94a3b8; font-size: 12px; margin: 0;">
                                © 2026 Shopyn Golden Store ERP. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
        
        msg.add_alternative(html_content, subtype='html')
        
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
            
        logger.info(f"Correo OTP enviado con éxito a {email_to}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo OTP a {email_to}: {e}")
        return False

def send_recovery_email(email_to: str, token: str):
    """
    Envía un correo con diseño HTML profesional para la recuperación de contraseña.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("Credenciales SMTP no configuradas. El correo no se enviará.")
        return False
        
    try:
        msg = EmailMessage()
        msg['Subject'] = '🔐 Recuperación de Contraseña - Shopyn Golden Store'
        msg['From'] = f"Shopyn Golden Store <{settings.SMTP_USER}>"
        msg['To'] = email_to
        
        link = f"http://localhost:4200/reset-password?token={token}"
        
        text_content = f"""Hola,

Has solicitado restablecer tu contraseña en Shopyn Golden Store.

Ingresa al siguiente enlace para restablecerla:
{link}

O utiliza tu token de seguridad para la app móvil:
{token}

Nota: Este enlace caducará en 15 minutos. Si no realizaste esta solicitud, puedes ignorar este mensaje.
"""
        msg.set_content(text_content)

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperación de Contraseña</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; padding: 40px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="background: linear-gradient(135deg, #e11d48 0%, #be123c 100%); padding: 35px 20px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 0.5px;">Shopyn Golden Store</h1>
                            <p style="color: #fecdd3; margin: 6px 0 0 0; font-size: 14px; font-weight: 500;">Recuperación de Contraseña</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px 35px;">
                            <h2 style="color: #1e293b; font-size: 20px; margin-top: 0; margin-bottom: 16px; font-weight: 600;">¿Solicitaste recuperar tu contraseña?</h2>
                            <p style="color: #475569; font-size: 15px; line-height: 1.6; margin-bottom: 24px;">
                                Hemos recibido una solicitud para restablecer la contraseña asociada a este correo electrónico.
                            </p>
                            <div align="center" style="margin: 30px 0;">
                                <a href="{link}" target="_blank" style="background-color: #e11d48; color: #ffffff; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 15px; display: inline-block;">
                                    Restablecer mi Contraseña
                                </a>
                            </div>
                            <div style="background-color: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 18px; margin: 25px 0; text-align: center;">
                                <p style="color: #64748b; font-size: 12px; margin: 0 0 8px 0; font-weight: 700; text-transform: uppercase;">Token para Aplicación Móvil (Flutter)</p>
                                <div style="font-family: monospace; font-size: 12px; color: #334155; word-break: break-all; background-color: #ffffff; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0; font-weight: bold;">
                                    {token}
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
        
        msg.add_alternative(html_content, subtype='html')
        
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
            
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo: {e}")
        return False

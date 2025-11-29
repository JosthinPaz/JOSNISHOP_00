import os
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

def enviar_alerta_stock(destinatario, producto, cantidad):
    remitente = "josnishop@gmail.com"
    password = "xzbd txnd hbwa ovjd"
    asunto = "¡Atención! Stock bajo en JosniShop"
    cuerpo = f"""
Hola,

Queremos informarte que el producto '{producto}' está por agotarse.
Actualmente solo quedan {cantidad} unidades disponibles.

Te recomendamos revisar el inventario y tomar las acciones necesarias en tu panel.

Saludos,
El equipo de JosniShop
"""
    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print("Error enviando correo:", e)

def enviar_confirmacion_compra(correo, pedido_id, pdf_bytes=None, filename=None):
    """Envía el correo de confirmación de compra. Acepta opcionalmente `pdf_bytes` para adjuntar la factura."""
    remitente = os.getenv('SMTP_EMAIL', 'josnishop@gmail.com')
    password = os.getenv('SMTP_PASSWORD', 'xzbd txnd hbwa ovjd')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '465'))

    asunto = "¡Gracias por tu compra en JosniShop!"
    cuerpo = f"""
Hola,

¡Tu compra ha sido confirmada exitosamente!
Tu número de pedido es: {pedido_id}

Adjuntamos la factura correspondiente en formato PDF.

Puedes consultar el estado de tu pedido en tu panel de usuario.

Gracias por confiar en JosniShop.
"""
    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = correo

    if pdf_bytes:
        if not filename:
            filename = f'factura_pedido_{pedido_id}.pdf'
        try:
            msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename=filename)
        except Exception as e:
            print('Error adjuntando PDF:', e)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(remitente, password)
            server.send_message(msg)
    except Exception as e:
        print("Error enviando correo:", e)

def send_registration_email(to_email):
    remitente = "josnishop@gmail.com"
    password = "xzbd txnd hbwa ovjd"
    subject = "Registro exitoso en JosniShop"
    body = (
        "¡Bienvenido a JosniShop!\n\n"
        "Te has registrado exitosamente y has aceptado los términos y condiciones del sistema.\n"
        "Gracias por confiar en nosotros."
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = remitente
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, to_email, msg.as_string())
    except Exception as e:
        print("Error enviando correo:", e)

def enviar_alerta_resena(destinatario, producto, comentario, calificacion):
    remitente = "josnishop@gmail.com"
    password = "xzbd txnd hbwa ovjd"
    asunto = "¡Nueva reseña en tu producto JosniShop!"
    cuerpo = f"""
Hola,

Has recibido una nueva reseña en tu producto '{producto}'.

Calificación: {calificacion} estrellas
Comentario: {comentario}

Revisa tu panel para responder o gestionar la reseña.

Saludos,
El equipo de JosniShop
"""
    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print("Error enviando correo:", e)


def enviar_respuesta_resena(destinatario, producto, respuesta_vendedor):
    """Enviar correo al cliente cuando el vendedor responde su reseña."""
    remitente = "josnishop@gmail.com"
    password = "xzbd txnd hbwa ovjd"
    asunto = "Tu reseña ha recibido una respuesta en JosniShop"
    cuerpo = f"""
Hola,

Tu reseña sobre el producto '{producto}' ha recibido una respuesta del vendedor:

Respuesta: {respuesta_vendedor}

Puedes ver la conversación en tu panel de usuario.

Saludos,
El equipo de JosniShop
"""
    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print("Error enviando correo (respuesta reseña):", e)


def enviar_cambio_estado_pedido(correo, pedido_id, nuevo_estado):
    """Enviar correo al cliente cuando cambie el estado de su pedido."""
    remitente = "josnishop@gmail.com"
    password = "xzbd txnd hbwa ovjd"
    asunto = f"Actualización de estado del pedido #{pedido_id}"
    cuerpo = f"""
Hola,

Te informamos que el estado de tu pedido #{pedido_id} ha cambiado a: {nuevo_estado}.

Puedes consultar más detalles en tu panel de usuario.

Gracias por comprar en JosniShop.
"""
    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = correo

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, correo, msg.as_string())
    except Exception as e:
        print("Error enviando correo (estado pedido):", e)
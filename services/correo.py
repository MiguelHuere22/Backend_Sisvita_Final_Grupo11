from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from model.persona import Persona
from model.usuario import Usuario

correos = Blueprint('correos', __name__)

@correos.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    data = request.json
    id_persona = data['id_persona']
    asunto = data['asunto']
    cuerpo = data['cuerpo']

    # Obtener el correo del usuario
    correo_persona = obtener_correo_persona(id_persona)

    if not correo_persona:
        return jsonify({"status_code": 400, "msg": "Correo no encontrado para la persona dada"}), 400

    destinatario = correo_persona

    # Configura tu servidor de correo aquí
    remitente = "IAGrupo8UNMSM@gmail.com"  # Reemplaza con tu correo electrónico real
    password = "ejltztoxmyfcuubb"  # Reemplaza con tu contraseña real

    try:
        msg = MIMEText(cuerpo)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())

        return jsonify({"status_code": 200, "msg": "Correo enviado exitosamente"}), 200

    except Exception as e:
        return jsonify({"status_code": 500, "msg": str(e)}), 500

def obtener_correo_persona(id_persona):
    persona = Persona.query.get(id_persona)
    if persona:
        usuario = Usuario.query.filter_by(id_persona=persona.id_persona).first()
        if usuario:
            return usuario.username  # Suponiendo que el username es el correo
    return None

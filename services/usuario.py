from flask import Blueprint, request, jsonify
from model.usuario import Usuario
from model.rol import Rol
from model.usuario_rol import UsuarioRol
from utils.db import db
from model.persona import Persona
from model.ubigeo import Ubigeo
usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/usuarios/v1', methods=['GET'])
def get_mensaje():
    result = {"data": 'Hola, Usuarios'}
    return jsonify(result)
@usuarios.route('/usuarios/v1/login/paciente', methods=['POST'])
def login_paciente():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    usuario = Usuario.query.filter_by(username=username, password=password).first()
    if usuario:
        usuario_rol = UsuarioRol.query.filter_by(id_usuario=usuario.id_usuario).first()
        rol = Rol.query.get(usuario_rol.id_rol)
        if rol.tipo_rol == 'Paciente':
            persona = Persona.query.get(usuario.id_persona)
            return jsonify({
                "status_code": 200,
                "msg": "Login successful",
                "data": {
                    "id_usuario": usuario.id_usuario,
                    "username": usuario.username,
                    "id_persona": usuario.id_persona,
                    "rol": rol.tipo_rol,
                    "persona": {
                        "id_persona": persona.id_persona,
                        "apellido_paterno": persona.apellido_paterno,
                        "apellido_materno": persona.apellido_materno,
                        "nombres": persona.nombres,
                        "sexo": persona.sexo,
                        "telefono": persona.telefono,
                        "fecha_nacimiento": persona.fecha_nacimiento.strftime('%Y-%m-%d')
                    }
                }
            }), 200
        else:
            return jsonify({
                "status_code": 403,
                "msg": "Unauthorized role"
            }), 403
    else:
        return jsonify({
            "status_code": 401,
            "msg": "Invalid credentials"
        }), 401


@usuarios.route('/usuarios/v1/login/especialista', methods=['POST'])
def login_especialista():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    usuario = Usuario.query.filter_by(username=username, password=password).first()
    if usuario:
        usuario_rol = UsuarioRol.query.filter_by(id_usuario=usuario.id_usuario).first()
        rol = Rol.query.get(usuario_rol.id_rol)
        if rol.tipo_rol == 'Especialista':
            persona = Persona.query.get(usuario.id_persona)
            ubigeo = Ubigeo.query.get(persona.id_ubigeo)  # Assuming you have a foreign key relationship

            return jsonify({
                "status_code": 200,
                "msg": "Login successful",
                "data": {
                    "id_usuario": usuario.id_usuario,
                    "username": usuario.username,
                    "id_persona": usuario.id_persona,
                    "rol": rol.tipo_rol
                },
                "personaData": {
                    "nombres": persona.nombres,
                    "apellido_paterno": persona.apellido_paterno,
                    "apellido_materno": persona.apellido_materno,
                    "sexo": persona.sexo,
                    "telefono": persona.telefono,
                    "departamento": ubigeo.departamento,
                    "provincia": ubigeo.provincia,
                    "distrito": ubigeo.distrito
                }
            }), 200
        else:
            return jsonify({
                "status_code": 403,
                "msg": "Unauthorized role"
            }), 403
    else:
        return jsonify({
            "status_code": 401,
            "msg": "Invalid credentials"
        }), 401


@usuarios.route('/usuarios/v1/listar', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    result = {
        "data": [usuario.__dict__ for usuario in usuarios],
        "status_code": 200,
        "msg": "Se recuperó la lista de Usuarios sin inconvenientes"
    }
    for usuario in result["data"]:
        usuario.pop('_sa_instance_state', None)  # Eliminar metadata de SQLAlchemy
    return jsonify(result), 200

@usuarios.route('/usuarios/v1/agregar', methods=['POST'])
def agregar_usuario():
    data = request.json
    nuevo_usuario = Usuario(
        username=data['username'],
        password=data['password'],
        id_persona=data['id_persona']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Asignar rol
    rol = Rol.query.filter_by(tipo_rol=data['rol']).first()
    if not rol:
        return jsonify({
            "status_code": 400,
            "msg": "Rol no válido"
        }), 400

    nuevo_usuario_rol = UsuarioRol(id_usuario=nuevo_usuario.id_usuario, id_rol=rol.id_rol)
    db.session.add(nuevo_usuario_rol)
    db.session.commit()

    return jsonify({
        "status_code": 201,
        "msg": "Usuario agregado exitosamente",
        "data": nuevo_usuario.__dict__
    }), 201

@usuarios.route('/usuarios/v1/actualizar/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get_or_404(id)
    usuario.username = data.get('username', usuario.username)
    usuario.password = data.get('password', usuario.password)
    usuario.id_persona = data.get('id_persona', usuario.id_persona)
    db.session.commit()

    # Actualizar rol
    if 'rol' in data:
        rol = Rol.query.filter_by(tipo_rol=data['rol']).first()
        if not rol:
            return jsonify({
                "status_code": 400,
                "msg": "Rol no válido"
            }), 400
        usuario_rol = UsuarioRol.query.filter_by(id_usuario=usuario.id_usuario).first()
        usuario_rol.id_rol = rol.id_rol
        db.session.commit()

    return jsonify({
        "status_code": 200,
        "msg": "Usuario actualizado exitosamente",
        "data": usuario.__dict__
    }), 200

@usuarios.route('/usuarios/v1/eliminar/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({
        "status_code": 200,
        "msg": "Usuario eliminado exitosamente"
    }), 200

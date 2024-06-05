from flask import Blueprint, request, jsonify
from model.estudiante import Estudiante
from utils.db import db

estudiantes = Blueprint('estudiantes', __name__)

@estudiantes.route('/estudiantes/v1', methods=['GET'])
def get_mensaje():
    result = {"data": 'Hola, Estudiantes'}
    return jsonify(result)
from flask import Blueprint, request, jsonify
from model.estudiante import Estudiante
from utils.db import db

estudiantes = Blueprint('estudiantes', __name__)

@estudiantes.route('/estudiantes/v1/login', methods=['POST'])
def login():
    data = request.json
    id_estudiante = data.get('id_estudiante')
    correo = data.get('correo')

    estudiante = Estudiante.query.filter_by(id_estudiante=id_estudiante, correo=correo).first()

    if estudiante:
        return jsonify({
            "status_code": 200,
            "msg": "Login successful",
            "data": {
                "id_estudiante": estudiante.id_estudiante,
                "apellido_paterno": estudiante.apellido_paterno,
                "apellido_materno": estudiante.apellido_materno,
                "nombres": estudiante.nombres,
                "sexo": estudiante.sexo,
                "correo": estudiante.correo,
                "telefono": estudiante.telefono,
                "fecha_nacimiento": estudiante.fecha_nacimiento.strftime('%Y-%m-%d')
            }
        }), 200
    else:
        return jsonify({
            "status_code": 401,
            "msg": "Invalid credentials"
        }), 401


@estudiantes.route('/estudiantes/v1/listar', methods=['GET'])
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    result = {
        "data": [estudiante.__dict__ for estudiante in estudiantes],
        "status_code": 200,
        "msg": "Se recuperó la lista de Estudiantes sin inconvenientes"
    }
    for estudiante in result["data"]:
        estudiante.pop('_sa_instance_state', None)  # Eliminar metadata de SQLAlchemy
    return jsonify(result), 200

@estudiantes.route('/estudiantes/v1/agregar', methods=['POST'])
def agregar_estudiante():
    data = request.json
    nuevo_estudiante = Estudiante(
        apellido_paterno=data['apellido_paterno'],
        apellido_materno=data['apellido_materno'],
        nombres=data['nombres'],
        sexo=data['sexo'],
        correo=data['correo'],
        telefono=data['telefono'],
        fecha_nacimiento=data['fecha_nacimiento']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({
        "status_code": 201,
        "msg": "Estudiante agregado exitosamente",
        "data": nuevo_estudiante.__dict__
    }), 201

@estudiantes.route('/estudiantes/v1/actualizar/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    data = request.json
    estudiante = Estudiante.query.get_or_404(id)
    estudiante.apellido_paterno = data.get('apellido_paterno', estudiante.apellido_paterno)
    estudiante.apellido_materno = data.get('apellido_materno', estudiante.apellido_materno)
    estudiante.nombres = data.get('nombres', estudiante.nombres)
    estudiante.sexo = data.get('sexo', estudiante.sexo)
    estudiante.correo = data.get('correo', estudiante.correo)
    estudiante.telefono = data.get('telefono', estudiante.telefono)
    estudiante.fecha_nacimiento = data.get('fecha_nacimiento', estudiante.fecha_nacimiento)
    db.session.commit()
    return jsonify({
        "status_code": 200,
        "msg": "Estudiante actualizado exitosamente",
        "data": estudiante.__dict__
    }), 200

@estudiantes.route('/estudiantes/v1/eliminar/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({
        "status_code": 200,
        "msg": "Estudiante eliminado exitosamente"
    }), 200


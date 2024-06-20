from flask import Blueprint, request, jsonify
from model.observacion import Observacion
from utils.db import db

observaciones = Blueprint('observaciones', __name__)

@observaciones.route('/observaciones/v1', methods=['GET'])
def get_mensaje():
    result = {"data": 'Hola, Observaciones'}
    return jsonify(result)

@observaciones.route('/observaciones/v1/listar', methods=['GET'])
def listar_observaciones():
    observaciones = Observacion.query.all()
    result = {
        "data": [observacion.to_dict() for observacion in observaciones],
        "status_code": 200,
        "msg": "Se recuperó la lista de Observaciones sin inconvenientes"
    }
    return jsonify(result), 200

@observaciones.route('/observaciones/v1/agregar', methods=['POST'])
def agregar_observacion():
    data = request.json
    nueva_observacion = Observacion(
        id_puntuacion=data['id_puntuacion'],
        id_especialista=data['id_especialista'],
        observaciones=data['observaciones'],
        nivel_ansiedad=data['nivel_ansiedad'],
        solicitud_cita=data['solicitud_cita']
    )
    db.session.add(nueva_observacion)
    db.session.commit()
    return jsonify({
        "status_code": 201,
        "msg": "Observación agregada exitosamente",
        "data": nueva_observacion.to_dict()
    }), 201

@observaciones.route('/observaciones/v1/actualizar/<int:id>', methods=['PUT'])
def actualizar_observacion(id):
    data = request.json
    observacion = Observacion.query.get_or_404(id)
    observacion.id_puntuacion = data.get('id_puntuacion', observacion.id_puntuacion)
    observacion.id_especialista = data.get('id_especialista', observacion.id_especialista)
    observacion.observaciones = data.get('observaciones', observacion.observaciones)
    observacion.nivel_ansiedad = data.get('nivel_ansiedad', observacion.nivel_ansiedad)
    observacion.solicitud_cita = data.get('solicitud_cita', observacion.solicitud_cita)
    db.session.commit()
    return jsonify({
        "status_code": 200,
        "msg": "Observación actualizada exitosamente",
        "data": observacion.to_dict()
    }), 200

@observaciones.route('/observaciones/v1/eliminar/<int:id>', methods=['DELETE'])
def eliminar_observacion(id):
    observacion = Observacion.query.get_or_404(id)
    db.session.delete(observacion)
    db.session.commit()
    return jsonify({
        "status_code": 200,
        "msg": "Observación eliminada exitosamente"
    }), 200



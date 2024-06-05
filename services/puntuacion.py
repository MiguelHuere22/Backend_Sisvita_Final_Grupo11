from flask import Blueprint, request, jsonify
from model.puntuacion import Puntuacion
from model.respuesta import Respuesta
from model.puntaje_opcion import PuntajeOpcion
from model.estudiante import Estudiante
from model.pregunta import Pregunta
from model.test import Test
from model.rango import Rango

from utils.db import db
puntuaciones = Blueprint('puntuaciones', __name__)

@puntuaciones.route('/puntuaciones/v1', methods=['GET'])
def get_mensaje():
    result = {"data": 'Hola, Puntuaciones'}
    return jsonify(result)

@puntuaciones.route('/puntuaciones/v1/calcular', methods=['POST'])
def calcular_puntuacion_total():
    data = request.json
    id_estudiante = data['id_estudiante']
    id_test = data['id_test']
    
    total_puntaje = db.session.query(db.func.sum(PuntajeOpcion.puntaje)).join(Respuesta, PuntajeOpcion.id_opcion == Respuesta.id_opcion).filter(
        Respuesta.id_estudiante == id_estudiante,
        PuntajeOpcion.id_pregunta.in_(db.session.query(Pregunta.id_pregunta).filter(Pregunta.id_test == id_test))
    ).scalar()
    
    estudiante = Estudiante.query.get(id_estudiante)
    test = Test.query.get(id_test)
    
    if not estudiante or not test:
        return jsonify({
            "status_code": 404,
            "msg": "Estudiante o Test no encontrado"
        }), 404
    
    # Obtener el rango correspondiente al puntaje total
    rango = Rango.query.filter(Rango.id_test == id_test, Rango.rango_min <= total_puntaje, Rango.rango_max >= total_puntaje).first()
    
    if not rango:
        interpretacion = "Rango no encontrado"
    else:
        interpretacion = rango.interpretacion

    return jsonify({
        "status_code": 200,
        "msg": "Puntuación total calculada exitosamente",
        "data": {
            "estudiante": {
                "id_estudiante": estudiante.id_estudiante,
                "apellido_paterno": estudiante.apellido_paterno,
                "apellido_materno": estudiante.apellido_materno,
                "nombres": estudiante.nombres,
                "sexo": estudiante.sexo,
                "correo": estudiante.correo,
                "telefono": estudiante.telefono,
                "fecha_nacimiento": estudiante.fecha_nacimiento.strftime('%Y-%m-%d')
            },
            "test": {
                #"id_test": test.id_test,
                "nombre": test.nombre,
                "descripcion": test.descripcion,
                "numero_preguntas": test.numero_preguntas
            },
            "total_puntaje": total_puntaje if total_puntaje else 0,
            "interpretacion": interpretacion
        }
    }), 200
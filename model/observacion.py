from utils.db import db
from dataclasses import dataclass

@dataclass
class Observacion(db.Model):
    id_observacion: int = db.Column(db.Integer, primary_key=True)
    id_puntuacion: int = db.Column(db.Integer, db.ForeignKey('puntuacion.id_puntuacion'), nullable=False)
    id_especialista: int = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=False)
    observaciones: str = db.Column(db.String(550))
    nivel_ansiedad: str = db.Column(db.String(50), nullable=False)
    solicitud_cita: str = db.Column(db.String(2), nullable=False)

    def __init__(self, id_puntuacion, id_especialista, observaciones, nivel_ansiedad, solicitud_cita):
        self.id_puntuacion = id_puntuacion
        self.id_especialista = id_especialista
        self.observaciones = observaciones
        self.nivel_ansiedad = nivel_ansiedad
        self.solicitud_cita = solicitud_cita

    def to_dict(self):
        return {
            "id_observacion": self.id_observacion,
            "id_puntuacion": self.id_puntuacion,
            "id_especialista": self.id_especialista,
            "observaciones": self.observaciones,
            "nivel_ansiedad": self.nivel_ansiedad,
            "solicitud_cita": self.solicitud_cita
        }
from utils.db import db
from dataclasses import dataclass

@dataclass
class Respuesta(db.Model):
    id_respuesta: int = db.Column(db.Integer, primary_key=True)
    id_estudiante: int = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_opcion: int = db.Column(db.Integer, db.ForeignKey('puntaje_opcion.id_opcion'), nullable=False)

    def __init__(self, id_estudiante, id_opcion):
        self.id_estudiante = id_estudiante
        self.id_opcion = id_opcion


from utils.db import db
from dataclasses import dataclass

@dataclass
class Puntuacion(db.Model):
    id_puntuacion: int = db.Column(db.Integer, primary_key=True)
    puntaje_total: int = db.Column(db.Integer, nullable=False)
    id_estudiante: int = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_test: int = db.Column(db.Integer, db.ForeignKey('test.id_test'), nullable=False)

    def __init__(self, puntaje_total, id_estudiante, id_test):
        self.puntaje_total = puntaje_total
        self.id_estudiante = id_estudiante
        self.id_test = id_test

from utils.db import db
from dataclasses import dataclass

@dataclass
class Estudiante(db.Model):
    id_estudiante: int = db.Column(db.Integer, primary_key=True)
    apellido_paterno: str = db.Column(db.String(50), nullable=False)
    apellido_materno: str = db.Column(db.String(50), nullable=False)
    nombres: str = db.Column(db.String(100), nullable=False)
    sexo: str = db.Column(db.String(1), nullable=False)
    correo: str = db.Column(db.String(100), nullable=False)
    telefono: str = db.Column(db.String(9), nullable=False)
    fecha_nacimiento: str = db.Column(db.Date, nullable=False)
    contraseña: str = db.Column(db.String(5), nullable=False) 

    def __init__(self, apellido_paterno, apellido_materno, nombres, sexo, correo, telefono, fecha_nacimiento, contraseña):
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nombres = nombres
        self.sexo = sexo
        self.correo = correo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.contraseña = contraseña


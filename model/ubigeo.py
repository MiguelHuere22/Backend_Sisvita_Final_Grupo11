from utils.db import db
from dataclasses import dataclass

@dataclass
class Ubigeo(db.Model):
    id_ubigeo: int = db.Column(db.Integer, primary_key=True)
    departamento: str = db.Column(db.String(50), nullable=False)
    provincia: str = db.Column(db.String(50))
    distrito: str = db.Column(db.String(50))
    superficie: float = db.Column(db.Numeric)
    altitud: float = db.Column(db.Numeric)
    latitud: float = db.Column(db.Numeric)
    longitud: float = db.Column(db.Numeric)

    def __init__(self, departamento, provincia, distrito, superficie, altitud, latitud, longitud):
        self.departamento = departamento
        self.provincia = provincia
        self.distrito = distrito
        self.superficie = superficie
        self.altitud = altitud
        self.latitud = latitud
        self.longitud = longitud

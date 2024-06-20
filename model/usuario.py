from utils.db import db
from dataclasses import dataclass

@dataclass
class Usuario(db.Model):
    id_usuario: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(100), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)
    id_persona: int = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=False)

    def __init__(self, username, password, id_persona):
        self.username = username
        self.password = password
        self.id_persona = id_persona

from flask import Flask
from flask_cors import CORS  # Importa CORS
from utils.db import db
from services.test import tests
from services.area import areas
from services.pregunta import preguntas
from services.respuesta import respuestas
from services.puntaje_opcion import puntajes_opciones
from services.rango import rangos
from services.puntuacion import puntuaciones
from services.persona import personas
from services.rol import roles
from services.ubigeo import ubigeos
from services.usuario import usuarios
from services.usuario_rol import usuarios_roles
from services.observacion import observaciones

from config import DATABASE_CONNECTION
from sqlalchemy import text


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Configura CORS para permitir todos los orígenes

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para desactivar las notificaciones de modificaciones de SQLAlchemy

# Inicializar SQLAlchemy
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(tests)
app.register_blueprint(areas)
app.register_blueprint(preguntas)
app.register_blueprint(respuestas)
app.register_blueprint(puntajes_opciones)
app.register_blueprint(rangos)
app.register_blueprint(puntuaciones)
app.register_blueprint(personas)
app.register_blueprint(roles)
app.register_blueprint(ubigeos)
app.register_blueprint(usuarios)
app.register_blueprint(usuarios_roles)
app.register_blueprint(observaciones)

with app.app_context():
    db.create_all()

#################### PARA PROBAR SI HAY CONEXIÓN
@app.route('/check_db')
def check_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            return 'Database connection successful!', 200
    except Exception as e:
        return str(e), 500
##########################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
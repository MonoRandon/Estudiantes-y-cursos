from app.config.mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "Llave_Secreta"

#importa y registra tus blueprint (controollers)

from app.controllers import cursos_controller
from app.controllers import estudiantes_controller

#registra los blueprints
app.register_blueprint(cursos_controller.cursos_bp)
app.register_blueprint(estudiantes_controller.estudiantes_bp)
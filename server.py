from app import app
from app.controllers import cursos_controller, estudiantes_controller

if __name__ == "__main__":
    app.run(debug=True, port=3008)

    

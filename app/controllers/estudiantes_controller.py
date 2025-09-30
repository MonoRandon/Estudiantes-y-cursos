#app/controllers/estudiantes_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.estudiante import Estudiante
from app.models.curso import Curso #NEcesitamos el modelo curso para el Dropdown

estudiantes_bp = Blueprint('estudiantes_bp', __name__)

@estudiantes_bp.route('/estudiante/new')
def new_estudiante():
    cursos = Curso.get_all()
    return render_template('nuevo_estudiante.html', cursos=cursos)

# Procesar creación de estudiante
@estudiantes_bp.route('/estudiante/create', methods=['POST'])
def create_estudiante():
    form = request.form.to_dict()
    # Convertir edad a int si viene como string
    if 'edad' in form:
        try:
            form['edad'] = int(form['edad'])
        except ValueError:
            form['edad'] = None
    if not Estudiante.validate_estudiante(form):
        return redirect(url_for('estudiantes_bp.new_estudiante'))
    Estudiante.save(form)
    flash('Estudiante creado exitosamente', 'success')
    return redirect(url_for('cursos_bp.index'))
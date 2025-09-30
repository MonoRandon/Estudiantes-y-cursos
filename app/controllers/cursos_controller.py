#app/controllers/cursos_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.curso import Curso

cursos_bp = Blueprint('cursos_bp', __name__)
# Rtuta para mostrar todos los cursos y el formulario de creacion

@cursos_bp.route('/')
@cursos_bp.route('/cursos')
def index():
    cursos = Curso.get_all()
    return render_template('cursos.html', cursos=cursos)

#Ruta para procesar la creacion de un nuevo curso
@cursos_bp.route('/cursos/new', methods=['POST'])
def create_curso():
    if not Curso.validate_curso(request.form):
        return redirect(url_for('cursos_bp.index'))
    data = {
        'nombre': request.form['nombre'],
        'descripcion': request.form['descripcion']
    }
    # Falta el método save en el modelo Curso, se debe agregar
    Curso.save(data)
    flash('Curso creado exitosamente', 'success')
    return redirect(url_for('cursos_bp.index'))

#Ruta para mostrar un curso especifico y sus estudiantes
@cursos_bp.route('/cursos/<int:curso_id>')
def show_curso(curso_id):
    curso = Curso.get_one_with_estudiantes(curso_id)
    if not curso:
        flash("Curso no encontrado", "error")
        return redirect(url_for('cursos.index'))
    return render_template('curso_detalle.html', curso=curso)

#Ruta para mostrar el formulario de edicion de un curso
@cursos_bp.route('/cursos/<int:curso_id>/edit')
def edit_curso(curso_id):
    curso = Curso.get_one_with_estudiantes(curso_id) #usamos el mismo metodo para obtener el curso
    if not curso:
        flash("Curso no encontrado", "error")
        return redirect(url_for('cursos.index'))
    return render_template('curso_editar.html', curso=curso)

#Ruta para procesar la edicion de un curso

@cursos_bp.route('/cursos/<int:curso_id>/update', methods=['POST'])
def update_curso(curso_id):
    if not Curso.validate_curso(request.form):
        return redirect(url_for('cursos.edit_curso', curso_id=curso_id))
    data = {
        'id': curso_id,
        'nombre': request.form['nombre'],
        'descripcion': request.form['descripcion']
    }

    Curso.update(data)
    flash("Curso actualizado con exito", "success")
    return redirect(url_for('cursos.show_curso', curso_id=curso_id))

#Ruta para eliminar un curso
@cursos_bp.route('cursos/<int:curso_id>/delete', methods=['POST'])
def delete_curso(curso_id):
    if Curso.delete(curso_id):
        flash("Curso eliminado con exito", "success")
    else:
        flash("Error al eliminar el curso", "error")
    return redirect(url_for('cursos.index'))

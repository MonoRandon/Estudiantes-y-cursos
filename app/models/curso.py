from flask import flash

from app.config.mysqlconnection import connectToMySQL

# nombre de tu base de datos (! asegurate de que coincida con la que creaste en MySQL)
DB_NAME = "esquema_estudiantes_cursos"

class Curso:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.estudiantes = [] #Para almacenar los estudiantes asociados 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cursos ORDER BY nombre ASC;"
        results = connectToMySQL(DB_NAME).query_db(query)
        cursos = []
        if results:
            for curso_data in results:
                cursos.append(cls(curso_data))
        return cursos

    @classmethod
    def get_one_with_estudiantes(cls, curso_id):
        query = '''
        SELECT c.*, e.id AS estudiante_id, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido, e.email AS estudiante_email, e.created_at AS estudiante_created_at, e.updated_at AS estudiante_updated_at
        FROM cursos c
        LEFT JOIN estudiantes e ON c.id = e.curso_id
        WHERE c.id = %(id)s;
        '''
        data = {'id': curso_id}
        results = connectToMySQL(DB_NAME).query_db(query, data)
        if not results:
            return None
        curso = cls(results[0])
        for row in results:
            if row['estudiante_id']:
                estudiante_data = {
                    'id': row['estudiante_id'],
                    'nombre': row['estudiante_nombre'],
                    'apellido': row['estudiante_apellido'],
                    'email': row['estudiante_email'],
                    'curso_id': row['id'],
                    'created_at': row['estudiante_created_at'],
                    'updated_at': row['estudiante_updated_at']
                }
                from app.models.estudiante import Estudiante
                curso.estudiantes.append(Estudiante(estudiante_data))
        return curso

        for row in results:
            if row['estudiante_id']:#si hay dattos del estudiantes
                estudiante_data = {
                'id': row['estudiante_id'],
                'nombre': row['estudiante_nombre'],
                'apellido': row['estudiante_apellido'],
                'email': row['estudiante_email'],
                'curso_id': row['id'], #El ID del curso al que pertenece
                'create_at': row['created_at'],# Estos campos no estan en el Select
                'updated_at': row['updated_at']

            }
                

            #importa el modelo Estudiante aqui para evitar importacion circular
            from app.models.estudiante import Estudiante
            curso.estudiantes.append(Estudiante(estudiante_data))

        return curso
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE cursos SET nombre = %(nombre)s, descripcion = %(descripcion)s, updated_at = NOW() WHERE id = %(id)s;"""

        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @classmethod
    def delete(cls, curso_id):
        query = "DELETE FROM cursos WHERE id = %(id)s;"
        data = {'id': curso_id}
        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @staticmethod
    def validate_curso(curso):
        is_valid = True
        if len(curso['nombre']) < 3:
            flash("El nombre del curso debe tener al menos 3 caracteres.", "curso_error")
            is_valid = False
            return is_valid
        
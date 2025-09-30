#app/models/estudiante.py

from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re #para validacion de email

#Nombre de tu base de datos
DB_NAME = "esquema_estudiantes_cursos"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Estudiante:
    def __init__ (self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.edad = data.get('edad')
        self.email = data['email']
        self.curso_id = data['curso_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO estudiantes (nombre, apellido, edad, email, curso_id) VALUES (%(nombre)s, %(apellido)s, %(edad)s, %(email)s, %(curso_id)s);"
        result = connectToMySQL(DB_NAME).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls, estudiante_id):
        query = "SELECT * FROM estudiantes WHERE id = %(id)s;"
        data = {'id': estudiante_id}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def update(cls, data):
        query = "UPDATE estudiantes SET nombre = %(nombre)s, apellido = %(apellido)s, edad = %(edad)s, email = %(email)s, curso_id = %(curso_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def delete(cls, estudiante_id):
        query = "DELETE FROM estudiantes WHERE id = %(id)s;"
        data = {'id': estudiante_id}
        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @staticmethod
    def validate_estudiante(estudiante):
        is_valid = True
        if len(estudiante['nombre']) < 2:
            flash("El nombre del estudiante debe tener al menos 2 caracteres.", "estudiante_error")
            is_valid = False
        if len(estudiante['apellido']) < 2:
            flash("El apellido del estudiante debe tener al menos 2 caracteres.", "estudiante_error")
            is_valid = False
        if not EMAIL_REGEX.match(estudiante['email']):
            flash("Email Inválido.", "estudiante_error")
            is_valid = False
        # Verificar si el email ya existe (opcional, buena práctica)
        query = "SELECT * FROM estudiantes WHERE email = %(email)s;"
        data = {'email': estudiante['email']}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        # Solo aplica si estamos editando, si hay 'id' en el form
        if result and ('id' not in estudiante or result[0]['id'] != int(estudiante['id'])):
            flash("El email ya está registrado.", "estudiante_error")
            is_valid = False
        if not estudiante.get('curso_id'):
            flash("Debe seleccionar un curso para el estudiante.", "estudiante_error")
            is_valid = False
        return is_valid
    
#config/mysql

import pymysql.cursors
class MySQLConnection:
    def __init__(self, db):
        try:
            connection = pymysql.connect(
                port = 3306,
                host='localhost',
                user = 'root', 
                password = 'admin4B',
                db = db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit= True
            )
            self.connection = connection
        except pymysql.Error as e:
            print(f"Error al conectar az la base de datos: {e}")
            self.connection = None # Establece la conexion en caso de error

    def query_db(self, query, data=None):
        if not self.connection:
            print("No hay conexión a la base de datos.")
            return False
        
        with self.connection.cursor() as cursor:
            try:
                if data:
                    print("Running query:", cursor.mogrify(query, data))
                
                cursor.execute(query, data)

                if query.lower().find("insert") >=0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >=0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit() #comit para update / Delete
                    return True #Para Update/Delete
            except Exception as e:
                print(f"Hubo un problema con la consulta: {e}")
                return False
            finally:
                pass #No cerramos la conexion aqui

    def connectToMySQL(db):
        return MySQLConnection(db)
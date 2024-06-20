from bd import Conexion as db
import json

class Especialidad:
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre

    def listar_especialidades(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre FROM especialidad ORDER BY nombre;"
        
        cursor.execute(sql)
        especialidades = cursor.fetchall()
        
        cursor.close()
        con.close()

        if especialidades:
            return json.dumps({'status': True, 'data': especialidades, 'message': 'Lista de especialidades'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay especialidades registradas'})

    def registrar_especialidad(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO especialidad (nombre) VALUES (%s);"
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.nombre])
            self.id = con.insert_id()
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Especialidad registrada correctamente'})

    def actualizar_especialidad(self):
        con = db().open
        cursor = con.cursor()
        sql = "UPDATE especialidad SET nombre = %s WHERE id = %s;"
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.nombre, self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        
        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Especialidad actualizada correctamente'})

    def eliminar_especialidad(self):
        con = db().open
        cursor = con.cursor()
        sql = "DELETE FROM especialidad WHERE id = %s;"
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        
        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Especialidad eliminada correctamente'})

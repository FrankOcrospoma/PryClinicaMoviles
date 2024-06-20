from bd import Conexion as db
import json

class DetalleEspecialidad:
    def __init__(self, odontologo_id=None, especialidad_id=None):
        self.odontologo_id = odontologo_id
        self.especialidad_id = especialidad_id

    def listar_detalles(self):
        con = db().open
        cursor = con.cursor()
        sql = """
        SELECT 
            d.odontologo_id, 
            d.especialidad_id, 
            u.nombre as odontologo_nombre, 
            e.nombre as especialidad_nombre 
        FROM detalle_especialidad d
        INNER JOIN usuario u ON d.odontologo_id = u.id
        INNER JOIN especialidad e ON d.especialidad_id = e.id;
        """
        
        cursor.execute(sql)
        detalles = cursor.fetchall()
        
        cursor.close()
        con.close()

        if detalles:
            return json.dumps({'status': True, 'data': detalles, 'message': 'Lista de detalles'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay detalles registrados'})

    def agregar_detalle(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO detalle_especialidad (odontologo_id, especialidad_id) VALUES (%s, %s);"
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.odontologo_id, self.especialidad_id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'message': 'Detalle agregado correctamente'})

    def eliminar_detalle(self):
        con = db().open
        cursor = con.cursor()
        sql = "DELETE FROM detalle_especialidad WHERE odontologo_id = %s AND especialidad_id = %s;"
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.odontologo_id, self.especialidad_id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        
        return json.dumps({'status': True, 'message': 'Detalle eliminado correctamente'})

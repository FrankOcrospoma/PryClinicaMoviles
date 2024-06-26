from bd import Conexion as db
import json
from decimal import Decimal

class Tratamiento:
    def __init__(self, id =None, nombre =None, descripcion =None, costo =None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo




    def listar_tratamientos(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre, descripcion, costo FROM tratamiento ORDER BY nombre;"

        cursor.execute(sql)
        tratamientos = cursor.fetchall()
        cursor.close()
        con.close()

        # Convertir objetos de tipo Decimal a float
        tratamientos_list = []
        for tratamiento in tratamientos:
            tratamiento_dict = dict(tratamiento)
            if isinstance(tratamiento_dict['costo'], Decimal):
                tratamiento_dict['costo'] = float(tratamiento_dict['costo'])
            tratamientos_list.append(tratamiento_dict)

        if tratamientos_list:
            return json.dumps({'status': True, 'data': tratamientos_list, 'message': 'Lista de tratamientos'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay tratamientos registrados'})

    def registrar_tratamiento(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO tratamiento (nombre, descripcion, costo) VALUES (%s, %s, %s);"

        try:
            con.autocommit = False
            cursor.execute(sql, [self.nombre, self.descripcion, self.costo])
            self.id = con.insert_id()
            con.commit()
            return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Tratamiento registrado correctamente'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

    def actualizar_tratamiento(self):
        con = db().open
        cursor = con.cursor()
        sql = "UPDATE tratamiento SET nombre = %s, descripcion = %s, costo = %s WHERE id = %s;"

        try:
            con.autocommit = False
            cursor.execute(sql, [self.nombre, self.descripcion, self.costo, self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close
            con.close()

        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Tratamiento actualizado correctamente'})

    def eliminar_tratamiento(self):
        con = db().open
        cursor = con.cursor()
        sql = "DELETE FROM tratamiento WHERE id = %s;"

        try:
            con.autocommit = False
            cursor.execute(sql, [self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close
            con.close()

        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Tratamiento eliminado correctamente'})
    
    @staticmethod
    def obtener_ids_por_nombres(nombres_tratamientos):
        con = db().open
        cursor = con.cursor()

        try:
            format_strings = ','.join(['%s'] * len(nombres_tratamientos))
            print("Query format strings:", format_strings)
            cursor.execute(f"SELECT id, nombre FROM tratamiento WHERE nombre IN ({format_strings})", tuple(nombres_tratamientos))
            resultados = cursor.fetchall()
            
            print("Resultados de la consulta:", resultados)
            
            # Convertir los resultados en un diccionario correctamente
            tratamientos_dict = {tratamiento['nombre']: tratamiento['id'] for tratamiento in resultados}
            
            cursor.close()
            con.close()
            return {'status': True, 'data': tratamientos_dict}, 200
        except Exception as e:
            print("Error:", e)
            cursor.close()
            con.close()
            return {'status': False, 'message': str(e)}, 500
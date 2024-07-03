from datetime import datetime
import mysql.connector
from flask import jsonify
import json
from bd import Conexion as db

class Notificacion:
    def __init__(self, usuario_id, mensaje):
        self.usuario_id = usuario_id
        self.mensaje = mensaje

    def registrar(self):
        # Abrir la conexión
        con = db().open
        
        # Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        # Preparar la sentencia de inserción
        sql = """
        INSERT INTO notificacion (
            usuario_id,
            mensaje,
            fecha,
            leida
        ) VALUES (%s, %s, %s, %s);
        """
        
        try:
            # Iniciar la operación, indicando que la transacción
            # se confirma de manera manual
            con.autocommit = False
            
            # Ejecutar la sentencia
            cursor.execute(sql, [self.usuario_id, self.mensaje, datetime.now(), 0])
            self.id = cursor.lastrowid
            
            # Confirmar la operación de agregar
            con.commit()
            
        except con.Error as error:  
            # Revocar la operación de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'notificacion_id': self.id}, 'message': 'Notificación registrada correctamente'})

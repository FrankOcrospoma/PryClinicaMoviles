from datetime import datetime
import mysql.connector
from flask import jsonify
import json
from bd import Conexion as db

class Notificacion:
    def __init__(self, usuario_id, mensaje):
        self.usuario_id = usuario_id
        self.mensaje = mensaje

    def registrar(self, cita_id):
        # Abrir la conexión
        con = db().open
        
        # Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        # Obtener el paciente_id basado en la cita_id
        cursor.execute("SELECT paciente_id FROM cita_atencion WHERE id = %s", (cita_id,))
        paciente_id_result = cursor.fetchone()

        if not paciente_id_result:
            cursor.close()
            con.close()
            return json.dumps({'status': False, 'message': 'Cita no encontrada con id: {}'.format(cita_id)})

        paciente_id = paciente_id_result['paciente_id']
        
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
            cursor.execute(sql, [paciente_id, self.mensaje, datetime.now(), 0])
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


    def listar_notificacion_paciente(self, paciente_id):
        con = db().open
        cursor = con.cursor()
        sql = """
            SELECT * FROM notificacion WHERE usuario_id= %s 
        """
        cursor.execute(sql, (paciente_id,))
        notificaciones = cursor.fetchall()
        cursor.close()
        con.close()
   
        if notificaciones:
            return json.dumps({'status': True, 'data': notificaciones, 'message': 'Lista de notificaciones'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay notificaciones registradas'})
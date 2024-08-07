from datetime import datetime
import mysql.connector
from flask import jsonify
import json
from bd import Conexion as db
from datetime import date, datetime
from util import CustomJsonEncoder

class Notificacion:
    def __init__(self, usuario_id=None, mensaje=None):
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

    def registrarPorEstado(self, cita_id):
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
        
        # Preparar la sentencia de inserción con verificación del estado de notificación
        sql = """
        INSERT INTO notificacion (usuario_id, mensaje, fecha, leida)
        SELECT u.id, %s, %s, %s
        FROM usuario u
        WHERE u.id = %s AND u.notificacion = 1;
        """
        
        try:
            # Iniciar la operación, indicando que la transacción
            # se confirma de manera manual
            con.autocommit = False
            
            # Ejecutar la sentencia
            cursor.execute(sql, [self.mensaje, datetime.now(), 0, paciente_id])
            
            # Confirmar la operación de agregar
            con.commit()
            
            self.id = cursor.lastrowid

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
            SELECT * FROM notificacion
            WHERE usuario_id = %s
            ORDER BY  fecha DESC
        """
        cursor.execute(sql, (paciente_id,))
        notificaciones = cursor.fetchall()
        cursor.close()
        con.close()

        notificaciones_list = []
        for notificacion in notificaciones:
            notificacion_dict = dict(notificacion)
            if isinstance(notificacion_dict.get('fecha'), datetime ):
                notificacion_dict['fecha'] = notificacion_dict['fecha'].strftime('%Y-%m-%d %H:%M:%S')
            notificaciones_list.append(notificacion_dict)
   
        if notificaciones_list:
            return json.dumps({'status': True, 'data': notificaciones_list, 'message': 'Lista de notificaciones'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay notificaciones registradas'})
        
    def listar_notificacion_paciente2(self, paciente_id):
        con = db().open
        cursor = con.cursor()
        sql = """
            SELECT * FROM notificacion
            WHERE usuario_id = %s
            ORDER BY leida ASC, fecha DESC
        """
        cursor.execute(sql, (paciente_id,))
        notificaciones = cursor.fetchall()
        cursor.close()
        con.close()

        notificaciones_list = []
        for notificacion in notificaciones:
            notificacion_dict = dict(notificacion)
            if isinstance(notificacion_dict.get('fecha'), datetime):
                notificacion_dict['fecha'] = notificacion_dict['fecha'].strftime('%Y-%m-%d %H:%M:%S')
            notificaciones_list.append(notificacion_dict)
   
        if notificaciones_list:
            return json.dumps({'status': True, 'data': notificaciones_list, 'message': 'Lista de notificaciones'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay notificaciones registradas'})
        

    #xddd
    def actualizar_notificacion_paciente(self, notificacion_id, leida):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """UPDATE notificacion SET leida = %s WHERE id = %s;"""
            cursor.execute(sql, (leida, notificacion_id))
            
            con.commit()
            return json.dumps({'status': True, 'data': {'notificacion_id': notificacion_id, 'leida': leida}, 'message': 'Notificación actualizado correctamente'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

#Anyelo
    def actualizar_estado_aea(self, notificacion_id, estado):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE notificacion SET leida = %s WHERE id = %s
            """
            cursor.execute(sql, (estado, notificacion_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})


    def actualizar_estado(self, notificacion_id, estado):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE notificacion SET leida = %s WHERE id = %s
            """
            cursor.execute(sql, (estado, notificacion_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})
    

    def registrarConVali(self, cita_id):
            # Abrir la conexión
            con = db().open
            
            # Crear un cursor que devuelve la consulta sql
            cursor = con.cursor()
            
            # Obtener el paciente_id basado en la cita_id
            cursor.execute("SELECT paciente_id FROM cita_atencion WHERE id = %s", (cita_id,))
            paciente_id_result = cursor.fetchone()

            print(paciente_id_result)
            if not paciente_id_result:
                cursor.close()
                con.close()
                return json.dumps({'status': False, 'message': 'Cita no encontrada con id: {}'.format(cita_id)})

            paciente_id = paciente_id_result['paciente_id']

            cursor.execute("SELECT notificacion FROM usuario WHERE id = %s", (paciente_id,))
            notificacion = cursor.fetchone()
            notificacion_id = notificacion['notificacion']
            print('Prueba',notificacion_id)
            if notificacion_id == 0:
                cursor.close()
                con.close()
                return json.dumps({'status': False, 'message': 'El usuario no quiere recibir notificaciones'})

            
            # Preparar la sentencia de inserción
            sql = """
            INSERT INTO notificacion (
                usuario_id,
                mensaje,
                fecha,
                leida
            ) VALUES (%s, %s, %s, %s);
            """
            print(sql)
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


    
    #Anyelo
    def registrarPorEstadoMejora(self):
        con = db().open
        
        cursor = con.cursor()

        cursor.execute("SELECT notificacion FROM usuario WHERE id = %s", (self.usuario_id,))
        notificacionResultado = cursor.fetchone()

        estadoNotificacion = notificacionResultado['notificacion']
        
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
            
            if estadoNotificacion == 1:

                cursor.execute(sql, [self.usuario_id, self.mensaje, datetime.now(), 0])
                
                self.id = cursor.lastrowid
                con.commit()
                return json.dumps({'status': True, 'data': {'notificacion_id': self.id}, 'message': 'Notificación registrada correctamente'})
            
            return json.dumps({'status': True, 'data': None, 'message': 'Notificación no registrada por inhabilitación de notificación'})
        except con.Error as error:  
            # Revocar la operación de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
        
            

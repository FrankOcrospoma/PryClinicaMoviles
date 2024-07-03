from bd import Conexion as db
import json
from util import CustomJsonEncoder
import os
import base64

class Atencion():
    def __init__(self, id=None, paciente_id=None, odontologo_id=None, fecha=None, hora=None, motivo_consulta=None, diagnostico=None, anotacion=None, costo=None, estado=None,cita_id=None):
        if cita_id is not None:
            self.cita_id = cita_id
            self.diagnostico = diagnostico
            self.anotacion = anotacion
        else:
            self.id = id
            self.paciente_id = paciente_id
            self.odontologo_id = odontologo_id
            self.fecha = fecha
            self.hora = hora
            self.motivo_consulta = motivo_consulta
            self.diagnostico = diagnostico
            self.anotacion = anotacion
            self.costo = costo
            self.estado = estado
        
    def Lista_Atencion(self):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            a.id AS atencion_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            CASE a.estado 
                WHEN 'R' THEN 'Realizada'
                WHEN 'C' THEN 'Cancelada'
                WHEN 'A' THEN 'Aplazada'
                WHEN 'P' THEN 'Programada'
                ELSE 'Estado desconocido'
            END AS estado
        FROM atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        ORDER BY a.fecha, a.hora;
        """
        
        cursor.execute(sql)
        #Recuperar los datos de la consulta SQL
        datos = cursor.fetchall()
        
        #Cerrar el cursor y la conexion
        cursor.close()
        con.close()
        datos_modificados = []
        for fila in datos:
            hora = fila['hora']  # Esto asume que 'hora' es un timedelta
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            fila_modificada = fila.copy()
            fila_modificada['hora'] = formatted_time
            datos_modificados.append(fila_modificada)

        print(datos_modificados)

        if datos_modificados:
            return json.dumps({'status': True, 'data': datos_modificados, 'message': 'Lista de atencion'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})

    def Lista_Atencion_PorEstado(self, estado):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            a.id AS atencion_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            CASE a.estado 
                WHEN 'R' THEN 'Realizada'
                WHEN 'C' THEN 'Cancelada'
                WHEN 'A' THEN 'Aplazada'
                WHEN 'P' THEN 'Programada'
                ELSE 'Estado desconocido'
            END AS estado
        FROM atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        WHERE a.estado = %s
        ORDER BY a.fecha, a.hora;
        """
        cursor.execute(sql, [estado])
        #Recuperar los datos de la consulta SQL
        datos = cursor.fetchall()
        
        #Cerrar el cursor y la conexion
        cursor.close()
        con.close()
        
        datos_modificados = []
        for fila in datos:
            hora = fila['hora']  # Esto asume que 'hora' es un timedelta
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            fila_modificada = fila.copy()
            fila_modificada['hora'] = formatted_time
            datos_modificados.append(fila_modificada)

        print(datos_modificados)

        if datos_modificados:
            return json.dumps({'status': True, 'data': datos_modificados, 'message': 'Lista de atencion'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
        
    def registrar(self):
        #Abrir la conexion
        con = db().open
        
        #Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        #Prepar la sentencia de actualziacion
        sql = """
        INSERT INTO atencion(
            paciente_id, 
            odontologo_id, 
            fecha, 
            hora, 
            motivo_consulta, 
            diagnostico, 
            anotacion, 
            costo, 
            estado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        try:
            #Iniciar la actualizacion, indicando que la operacion (Transaccion)
            #Se confirma de manera manual
            con.autocommit = False
            #Ejecutar la sentencia
            cursor.execute(sql, [self.paciente_id, self.odontologo_id, self.fecha,self.hora, self.motivo_consulta, self.diagnostico,self.anotacion, self.costo, self.estado])
            self.id = con.insert_id()  

            #Confirmar la operacion de agregar
            con.commit()
            
        except con.Error as error:  
            #Revocar la operacion de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'atencion_id': self.id}, 'message': 'Atencion registrada correctamente'})

    def actualizar_atencion(self):
            # Abrir la conexión
            con = db().open
            
            # Crear un cursor para ejecutar la consulta SQL
            cursor = con.cursor()
            
            # Preparar la sentencia de actualización
            sql = """UPDATE atencion SET paciente_id = %s, odontologo_id = %s, fecha = %s, 
                    hora = %s, motivo_consulta = %s, diagnostico = %s, anotacion = %s, 
                    costo = %s, estado = %s WHERE id = %s"""
            
            try:
                # Iniciar la actualización, indicando que la operación (Transacción)
                # se confirma de manera manual
                con.autocommit = False
                
                # Ejecutar la sentencia
                cursor.execute(sql, [self.paciente_id, self.odontologo_id, self.fecha, self.hora,
                                    self.motivo_consulta, self.diagnostico, self.anotacion,
                                    self.costo, self.estado, self.id])
                
                # Confirmar la operación de actualizar
                con.commit()
                
            except con.Error as error:
                # Revocar la operación de agregar
                con.rollback()
                
                return json.dumps({'status': False, 'data': None, 'message': str(error)})
            
            finally:
                # Cerrar el cursor y la conexión
                cursor.close()
                con.close()
                
            return json.dumps({'status': True, 'data': {'atencion_id': self.id}, 'message': 'Atención eliminada correctamente'})
        
    def eliminar_atencion(self):
        # Abrir la conexión
        con = db().open
        
        # Crear un cursor que ejecuta la consulta SQL
        cursor = con.cursor()
        
        # Preparar la sentencia de eliminación
        sql = "DELETE FROM atencion WHERE id = %s"
        
        try:
                # Iniciar la operación, indicando que la transacción
                # se confirma de manera manual
                con.autocommit = False
                
                # Ejecutar la sentencia
                cursor.execute(sql, [self.id])

                # Confirmar la operación
                con.commit()
                
        except con.Error as error:
                # Revocar la operación en caso de error
                con.rollback()
                
                return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
                # Cerrar el cursor y la conexión
                cursor.close()
                con.close()
                
        return json.dumps({'status': True, 'data': {'atencion_id': self.id}, 'message': 'Atención eliminada correctamente'})


    #APIS para paciente

    def registrar_cita_atencion_por_paciente(self):
        con = db().open
        
        cursor = con.cursor()
        
        sql = """
        INSERT INTO cita_atencion(
                paciente_id, 
                odontologo_id, 
                fecha, 
                hora, 
                motivo_consulta,
                id_estado_cita,
                costo
        ) VALUES (%s, %s, %s, %s, %s, (SELECT id FROM estado_cita_atencion WHERE estado = 'PROGRAMADA'), 50.00);
        """
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.paciente_id, self.odontologo_id, self.fecha, self.hora, self.motivo_consulta])
            self.id = con.insert_id()  
            con.commit()
                
        except con.Error as error:
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
                
        return json.dumps({'status': True, 'data': {'atencion_id': self.id}, 'message': 'Cita registrada correctamente'})
    

    def obtener_citas_por_paciente(self, paciente_id):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            a.id AS cita_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            e.estado AS estado
        FROM cita_atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        INNER JOIN estado_cita_atencion e on e.id = a.id_estado_cita
        WHERE a.paciente_id=%s AND (e.estado='PROGRAMADA' or e.estado='APLAZADA')
        ORDER BY a.fecha, a.hora;
        """
        
        cursor.execute(sql, paciente_id)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()
        datos_modificados = []
        for fila in datos:
            hora = fila['hora']
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            fila_modificada = fila.copy()
            fila_modificada['hora'] = formatted_time
            datos_modificados.append(fila_modificada)

        if datos_modificados:
            return json.dumps({'status': True, 'data': datos_modificados, 'message': 'Lista de citas programadas'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
        
        
    def obtener_citas(self):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            a.id AS cita_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            e.estado AS estado
        FROM cita_atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        INNER JOIN estado_cita_atencion e on e.id = a.id_estado_cita
        WHERE e.estado='PROGRAMADA' or e.estado='APLAZADA'
        ORDER BY a.fecha, a.hora;
        """
        
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()
        datos_modificados = []
        for fila in datos:
            hora = fila['hora']
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            fila_modificada = fila.copy()
            fila_modificada['hora'] = formatted_time
            datos_modificados.append(fila_modificada)

        if datos_modificados:
            return json.dumps({'status': True, 'data': datos_modificados, 'message': 'Lista de citas programadas'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
        
    def obtenerPacientes(self):
        con = db().open
        
        cursor = con.cursor() 
        
        
        sql = """
        select * from usuario
        WHERE rol_id = 2 and estado = 1;
        """
        
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'pacientes'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
             
    def obtenerOdontologos(self):
        con = db().open
        
        cursor = con.cursor() 
        
        
        sql = """
        select * from usuario
        WHERE rol_id = 3;
        """
        
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'odontologos'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
             

    def reprogramar_cita_atencion_por_paciente(self):
        con = db().open
        
        cursor = con.cursor()
        
        sql = """
        UPDATE cita_atencion
        SET 
            fecha = %s,
            hora = %s,
            id_estado_cita = (SELECT id FROM estado_cita_atencion WHERE estado = 'APLAZADA')
        WHERE id = %s;
        """
        
        try:
            con.autocommit = False
            cursor.execute(sql, [self.fecha, self.hora, self.id])
            con.commit()
                
        except con.Error as error:
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
                
        return json.dumps({'status': True, 'data': {'cita_id': self.id}, 'message': 'Cita aplazada correctamente'})
    

    def obtener_historial_por_paciente(self, paciente_id):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            c.id, 
            c.fecha, 
            c.hora, 
            c.diagnostico, 
            c.anotacion, 
            (SELECT CONCAT(nombre, ' ', ape_completo) FROM usuario WHERE id=c.odontologo_id) AS odontologo 
        FROM cita_atencion c
            INNER JOIN usuario u ON u.id=c.paciente_id
            INNER JOIN estado_cita_atencion e ON e.id=c.id_estado_cita
            WHERE c.paciente_id=%s AND e.estado="REALIZADA"
        """
        
        cursor.execute(sql, paciente_id)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Historial médico'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
     

    def obtener_detalle_historial_por_paciente(self, cita_id):
        con = db().open
        
        cursor = con.cursor() 
        
        detalle_historial = {}

        sql_tratamiento = """
        SELECT
            t.nombre AS tratamiento, 
            t.descripcion AS descripcion_tratamiento, 
            t.costo AS costo_tratamiento
        FROM cita_atencion c
        INNER JOIN atencion_tratamiento a ON a.atencion_id = c.id
        INNER JOIN tratamiento t ON a.tratamiento_id = t.id
        WHERE c.id = %s;
        """
        sql_receta = """SELECT id AS receta_id, medicamento, dosis FROM receta 
	        WHERE atencion_id = %s;
        """
        
        
        cursor.execute(sql_tratamiento, cita_id)
        datos_tratamiento = cursor.fetchall()
        
        detalle_historial["tratamientos"] = datos_tratamiento

        cursor.execute(sql_receta, cita_id)
        datos_receta= cursor.fetchall()

        detalle_historial["recetas"] = datos_receta

        cursor.close()
        con.close()

        if detalle_historial:
            return json.dumps({'status': True, 'data': detalle_historial, 'message': 'Detalle historial médico'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
        
    def obtener_detalle_historial_por_paciente2(self, cita_id):
        con = db().open
        
        cursor = con.cursor() 
        
        detalle_historial = {}
        
        # Obtener el paciente_id basado en la cita_id
        cursor.execute("SELECT paciente_id FROM cita_atencion WHERE id = %s", (cita_id,))
        paciente_id_result = cursor.fetchone()

        if not paciente_id_result:
            cursor.close()
            con.close()
            return json.dumps({'status': False, 'message': 'Cita no encontrada con id: {}'.format(cita_id)})

        paciente_id = paciente_id_result['paciente_id']
        
        sql_tratamiento = """
        SELECT
            t.nombre AS tratamiento, 
            t.descripcion AS descripcion_tratamiento, 
            t.costo AS costo_tratamiento,
            c.fecha
        FROM cita_atencion c
        INNER JOIN atencion_tratamiento a ON a.atencion_id = c.id
        INNER JOIN tratamiento t ON a.tratamiento_id = t.id
        INNER JOIN usuario u ON u.id = c.paciente_id
        WHERE u.id = %s;
        """
        sql_receta = """SELECT receta.id AS receta_id, receta.medicamento, receta.dosis,c.fecha FROM receta INNER JOIN cita_atencion c ON receta.atencion_id=c.id INNER JOIN usuario u ON u.id = c.paciente_id
        wHERE u.id = %s;
        """
        
        
        cursor.execute(sql_tratamiento, paciente_id)
        datos_tratamiento = cursor.fetchall()
        
        detalle_historial["tratamientos"] = datos_tratamiento

        cursor.execute(sql_receta, paciente_id)
        datos_receta= cursor.fetchall()

        detalle_historial["recetas"] = datos_receta

        

        cursor.close()
        con.close()

        if detalle_historial:
            return json.dumps({'status': True, 'data': detalle_historial, 'message': 'Detalle historial médico'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
     

    def obtener_odontologos(self):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT u.id, CONCAT(u.nombre, ' ', u.ape_completo) as nombre_completo
        FROM usuario u 
        INNER JOIN rol r ON u.rol_id=r.id
        WHERE r.nombre = 'odontologo' AND u.estado=1;
        """
        
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()


        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Lista de odontólogos activos'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
       

    def cancelar_cita_atencion_por_paciente(self):
        con = db().open
        
        cursor = con.cursor()
        
        sql = """
        UPDATE cita_atencion
        SET 
        id_estado_cita = (SELECT id FROM estado_cita_atencion WHERE estado = "CANCELADA")
        WHERE id = %s;
        """
        
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
                
        return json.dumps({'status': True, 'data': {'cita_id': self.id}, 'message': 'Cita cancelada correctamente'})
    
    
    
    def obtener_citas_por_odontologo(self, odontologo_id):
        con = db().open
        
        cursor = con.cursor() 
        
        sql = """
        SELECT 
            a.id AS cita_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            e.estado AS estado
        FROM cita_atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        INNER JOIN estado_cita_atencion e on e.id = a.id_estado_cita
        WHERE a.odontologo_id=%s AND (e.estado='PROGRAMADA' OR e.estado='APLAZADA')
        ORDER BY a.fecha, a.hora;
        """
        
        cursor.execute(sql, (odontologo_id,))
        datos = cursor.fetchall()
        
        cursor.close()
        con.close()
        datos_modificados = []
        for fila in datos:
            hora = fila['hora']
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            fila_modificada = fila.copy()
            fila_modificada['hora'] = formatted_time
            datos_modificados.append(fila_modificada)

        if datos_modificados:
            return json.dumps({'status': True, 'data': datos_modificados, 'message': 'Lista de citas programadas'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'Sin registros'})
        
        
        
    def obtener_cita_por_id(self, cita_id):
        con = db().open

        cursor = con.cursor()

        sql = """
        SELECT 
            a.id AS cita_id,
            CONCAT(p.nombre, ' ', p.ape_completo) AS nombre_paciente,
            CONCAT(o.nombre, ' ', o.ape_completo) AS nombre_odontologo,
            a.fecha,
            a.hora,
            a.motivo_consulta,
            a.diagnostico,
            a.anotacion,
            a.costo,
            e.estado AS estado
        FROM cita_atencion a
        INNER JOIN usuario p ON a.paciente_id = p.id
        INNER JOIN usuario o ON a.odontologo_id = o.id
        INNER JOIN estado_cita_atencion e on e.id = a.id_estado_cita
        WHERE a.id=%s;
        """

        cursor.execute(sql, (cita_id,))
        datos = cursor.fetchone()

        cursor.close()
        con.close()
        
        if datos:
            hora = datos['hora']
            formatted_time = f"{hora.seconds // 3600:02}:{(hora.seconds % 3600) // 60:02}:{hora.seconds % 60:02}"
            datos['hora'] = formatted_time
            return json.dumps({'status': True, 'data': datos, 'message': 'Detalle de la cita'}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': {}, 'message': 'Cita no encontrada'})
        
    def actualizar_cita(self):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE cita_atencion
            SET diagnostico = COALESCE(%s, diagnostico),
                anotacion = COALESCE(%s, anotacion)
            WHERE id = %s
            """
            cursor.execute(sql, (self.diagnostico, self.anotacion, self.cita_id))
            con.commit()
            cursor.close()
            con.close()
            return json.dumps({'status': True, 'message': 'Cita actualizada exitosamente'})
        except Exception as e:
            con.rollback()
            cursor.close()
            con.close()
            return json.dumps({'status': False, 'message': str(e)})


    
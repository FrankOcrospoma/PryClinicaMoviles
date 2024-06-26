from bd import Conexion as db
import json
from decimal import Decimal
from datetime import date, time, datetime, timedelta

class Pago:
    def __init__(self, id=None, monto=None, estado=None, atencion_id=None):
        self.id = id
        self.monto = monto
        self.estado = estado
        self.atencion_id = atencion_id

    def listar_pagos(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, monto, estado, atencion_id FROM pago ORDER BY id;"

        cursor.execute(sql)
        pagos = cursor.fetchall()
        cursor.close()
        con.close()

        # Convertir objetos de tipo Decimal a float
        pagos_list = []
        for pago in pagos:
            pago_dict = dict(pago)
            if isinstance(pago_dict['monto'], Decimal):
                pago_dict['monto'] = float(pago_dict['monto'])
            pagos_list.append(pago_dict)

        if pagos_list:
            return json.dumps({'status': True, 'data': pagos_list, 'message': 'Lista de pagos'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay pagos registrados'})

    def registrar_pago(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO pago (monto, estado, atencion_id) VALUES (%s, %s, %s);"

        try:
            con.autocommit = False
            cursor.execute(sql, [self.monto, self.estado, self.atencion_id])
            self.id = con.insert_id()
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Pago registrado correctamente'})

    def actualizar_pago(self):
        con = db().open
        cursor = con.cursor()
        sql = "UPDATE pago SET monto = %s, estado = %s, atencion_id = %s WHERE id = %s;"

        try:
            con.autocommit = False
            cursor.execute(sql, [self.monto, self.estado, self.atencion_id, self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Pago actualizado correctamente'})

    def eliminar_pago(self):
        con = db().open
        cursor = con.cursor()
        sql = "DELETE FROM pago WHERE id = %s;"

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

        return json.dumps({'status': True, 'data': {'id': self.id}, 'message': 'Pago eliminado correctamente'})


#APIS PARA APP PACIENTE

    def listar_pagos_pendientes(self, paciente_id):
        con = db().open
        cursor = con.cursor()
        sql = """
        SELECT 
            c.id AS cita_id, 
            c.fecha, 
            c.hora, 
            (SELECT UPPER(CONCAT(nombre, ' ', ape_completo)) FROM usuario WHERE id = c.odontologo_id) AS nombre_odontologo,
            c.motivo_consulta, 
            SUM(dp.costo) AS costo,
            (SELECT COUNT(*) FROM detalle_pago WHERE cita_id= c.id) -1 AS cantidad_tratamiento
        FROM cita_atencion c
        INNER JOIN detalle_pago dp ON c.id = dp.cita_id
        WHERE c.paciente_id = %s 
        AND dp.estado_pago_id = (SELECT id FROM estado_cita_atencion WHERE estado = 'PENDIENTE')
        GROUP BY 
            c.id, 
            c.fecha, 
            c.hora, 
            nombre_odontologo, 
            c.motivo_consulta
        """
        cursor.execute(sql, (paciente_id,))
        pagos = cursor.fetchall()
        cursor.close()
        con.close()

        # Convertir objetos de tipo Decimal a float y date/time/timedelta a string
        pagos_list = []
        for pago in pagos:
            pago_dict = dict(pago)
            for key, value in pago_dict.items():
                if isinstance(value, Decimal):
                    pago_dict[key] = float(value)
                elif isinstance(value, (date, time, datetime)):
                    pago_dict[key] = value.isoformat()
                elif isinstance(value, timedelta):
                    pago_dict[key] = str(value)
            pagos_list.append(pago_dict)

        if pagos_list:
            return json.dumps({'status': True, 'data': pagos_list, 'message': 'Lista de pagos pendientes'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay pagos registrados'})
        

    def listar_detalle_pago_cita(self, cita_id):
        con = db().open
        cursor = con.cursor()
        sql = """
        SELECT 
            dp.detalle_pago_id,
            c.id AS cita_id,
            pago_id,
            dp.atencion_tratamiento_id,
            CASE 
            WHEN dp.atencion_tratamiento_id IS NULL THEN 'Consulta'
            ELSE (SELECT nombre FROM tratamiento WHERE id=dp.atencion_tratamiento_id)
        END AS servicio,
            dp.costo AS costo,
            (SELECT estado FROM estado_cita_atencion WHERE id = dp.estado_pago_id) AS estado
        FROM cita_atencion c
        INNER JOIN detalle_pago dp ON c.id = dp.cita_id
        WHERE c.id = %s AND dp.estado_pago_id =  (SELECT id FROM estado_cita_atencion WHERE estado = 'PENDIENTE')
        """
        cursor.execute(sql, (cita_id,))
        pagos = cursor.fetchall()
        cursor.close()
        con.close()

        # Convertir objetos de tipo Decimal a float y date/time/timedelta a string
        pagos_list = []
        for pago in pagos:
            pago_dict = dict(pago)
            for key, value in pago_dict.items():
                if isinstance(value, Decimal):
                    pago_dict[key] = float(value)
            pagos_list.append(pago_dict)

        if pagos_list:
            return json.dumps({'status': True, 'data': pagos_list, 'message': 'Lista de detalle pago por cita'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay pagos registrados'})
        
    def registrar_detalle_pago(self, detalle_pago):
        try:
            con = db().open
            cursor = con.cursor()
            data_detalle_pago = json.loads(detalle_pago)

            con.autocommit = False

            sql_pago_update = """
            UPDATE pago 
            SET 
                monto = %s, 
                estado_id = (SELECT id FROM estado_cita_atencion WHERE estado = 'REALIZADA') 
            WHERE 
                id = %s;
            """
            sql_detalle_pago_update = """
            UPDATE detalle_pago
            SET
                estado_pago_id = (SELECT id FROM estado_cita_atencion WHERE estado = 'REALIZADA'),
                pago_id = %s
            WHERE 
                detalle_pago_id = %s;
            """

            sql_pago_crear = """
            INSERT INTO pago (monto, estado_id) VALUES(%s,  (SELECT id FROM estado_cita_atencion WHERE estado = 'PENDIENTE'));
            """
            
            
            existencia_consulta = False 
            monto_total = 0 
            pago_id = None  # Inicializar pago_id

            for item in data_detalle_pago:
                if item["servicio"].upper() == "CONSULTA":
                    existencia_consulta = True
                    pago_id = item["pago_id"]

                monto_total += float(item["costo"])

            if existencia_consulta and pago_id is not None:
                cursor.execute(sql_pago_update, (monto_total, pago_id))
                for item in data_detalle_pago:
                    cursor.execute(sql_detalle_pago_update, (pago_id, item["detalle_pago_id"]))
                
                con.commit()
                return json.dumps({'status': True, 'data': None, 'message': 'Pago registrado correctamente'})


            cursor.execute(sql_pago_crear, (monto_total, ))
            pago_id = con.insert_id()
            for item in data_detalle_pago:
                cursor.execute(sql_detalle_pago_update, (pago_id, item["detalle_pago_id"]))
            
            con.commit()
            return json.dumps({'status': True, 'data': None, 'message': 'Pago registrado correctamente'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

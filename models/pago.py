from bd import Conexion as db
import json
from decimal import Decimal

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

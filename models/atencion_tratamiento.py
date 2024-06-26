from bd import Conexion as db
import json
from util import CustomJsonEncoder
import os
import base64
class AtencionTratamiento:
    def __init__(self, cita_id, tratamiento_id):
        self.cita_id = cita_id
        self.tratamiento_id = tratamiento_id

    def registrar_atencion_tratamiento(self):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            INSERT INTO atencion_tratamiento (atencion_id, tratamiento_id,estado)
            VALUES (%s, %s,'5')
            """
            cursor.execute(sql, (self.cita_id, self.tratamiento_id))
            con.commit()
            cursor.close()
            con.close()
            return json.dumps({'status': True, 'message': 'Tratamiento registrado exitosamente'})
        except Exception as e:
            con.rollback()
            cursor.close()
            con.close()
            return json.dumps({'status': False, 'message': str(e)})

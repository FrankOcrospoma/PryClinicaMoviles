from bd import Conexion as db
import json
from decimal import Decimal
from datetime import date, time, datetime, timedelta

class Receta:
    def __init__(self, cita_id, medicamento, dosis):
        self.cita_id = cita_id
        self.medicamento = medicamento
        self.dosis = dosis

    def registrar_receta(self):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            INSERT INTO receta (atencion_id, medicamento, dosis)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (self.cita_id, self.medicamento, self.dosis))
            con.commit()
            cursor.close()
            return json.dumps({'status': True, 'message': 'Receta registrada exitosamente'})
        except Exception as e:
            con.rollback()
            cursor.close()
            return json.dumps({'status': False, 'message': str(e)})
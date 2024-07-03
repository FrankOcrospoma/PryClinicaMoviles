from bd import Conexion as db
import json

class SeguroDental:
  def __init__(self, id=None, nombre_compania=None, tipo_cobertura=None, telefono_compania=None, paciente_id=None):
      self.id = id
      self.nombre_compania = nombre_compania
      self.tipo_cobertura = tipo_cobertura
      self.telefono_compania = telefono_compania
      self.paciente_id = paciente_id

  def obtener_seguro_dental(self, paciente_id):
    con = db().open
    cursor = con.cursor()

    sql = "SELECT id AS seguro_dental_id, nombre_compania, tipo_cobertura, telefono_compania FROM seguro_dental WHERE paciente_id = %s"
    try:
      cursor.execute(sql, [paciente_id])
      data = cursor.fetchall()
      con.commit()

      if data:
        return json.dumps({'status': True, 'data': data, 'message': 'Seguro dental de paciente'})
      else:
        return json.dumps({'status': False, 'data': None, 'message': 'Sin registros de seguro dental'})
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()


  def agregar_seguro(self):
    con = db().open
    cursor = con.cursor()

    sql = "INSERT INTO seguro_dental(nombre_compania, tipo_cobertura, telefono_compania, paciente_id) VALUES (%s, %s, %s, %s)"
    try:
      con.autocommit = False
      cursor.execute(sql, [self.nombre_compania, self.tipo_cobertura, self.telefono_compania, self.paciente_id])
      con.commit()
      self.id = cursor.lastrowid
      return json.dumps({'status': True, 'data': {'seguro_id': self.id}, 'message': 'Seguro dental agregado correctamente'})
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()

  def actualizar_seguro(self):
    con = db().open
    cursor = con.cursor()

    sql = "UPDATE seguro_dental SET nombre_compania = %s, tipo_cobertura = %s, telefono_compania = %s WHERE id = %s"
    try:
      con.autocommit = False
      cursor.execute(sql, [self.nombre_compania, self.tipo_cobertura, self.telefono_compania, self.id])
      con.commit()
      return json.dumps({'status': True, 'data': {'seguro_id': self.id}, 'message': 'Seguro dental actualizado correctamente'})
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()

  def eliminar_seguro(self):
    con = db().open
    cursor = con.cursor()

    sql = "DELETE FROM seguro_dental WHERE id = %s"
    try:
      con.autocommit = False
      cursor.execute(sql, [self.id])
      con.commit()
      return json.dumps({'status': True, 'data': {'seguro_id': self.id}, 'message': 'Seguro dental eliminado correctamente'})
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()

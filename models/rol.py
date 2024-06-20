from bd import Conexion as db
import json

class Rol():
  def __init__(self, id=None, nombre=None):
    self.id = id
    self.nombre = nombre

  def listar_roles(self):
    con = db().open
    cursor = con.cursor()
    sql = "SELECT id, nombre FROM rol"
    cursor.execute(sql)
    roles = cursor.fetchall()
    cursor.close()
    con.close()
    if roles:
      return json.dumps({'status': True, 'data': roles, 'message': 'Lista de roles'})
    else:
      return json.dumps({'status': False, 'data': None, 'message': 'Sin registros de roles'})

  def agregar_rol(self):
    con = db().open
    cursor = con.cursor()
    sql = "INSERT INTO rol(nombre) VALUES (%s)"
    try:
      cursor.execute(sql, [self.nombre])
      self.id = con.insert_id()
      con.commit()
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()
    return json.dumps({'status': True, 'data': {'rol_id':self.id}, 'message': 'Rol agregado correctamente'})

  def actualizar_rol(self):
    con = db().open
    cursor = con.cursor()
    sql = "UPDATE rol SET nombre = %s WHERE id = %s"
    try:
      cursor.execute(sql, [self.nombre, self.id])

      con.commit()
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()
    return json.dumps({'status': True, 'data': {'rol_id':self.id}, 'message': 'Rol actualizado correctamente'})

  def eliminar_rol(self):
    con = db().open
    cursor = con.cursor()
    sql = "DELETE FROM rol WHERE id = %s"
    try:
      cursor.execute(sql, [self.id])
      con.commit()
    except con.Error as error:
      con.rollback()
      return json.dumps({'status': False, 'data': None, 'message': str(error)})
    finally:
      cursor.close()
      con.close()
    return json.dumps({'status': True, 'data': {'rol_id':self.id}, 'message': 'Rol eliminado correctamente'})

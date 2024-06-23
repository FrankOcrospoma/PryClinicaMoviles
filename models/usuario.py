from bd import Conexion as db
import json
from datetime import date
from util import CustomJsonEncoder

class Usuario():
    def __init__(self, id=None, nombreUsuario=None, email=None, contrasena=None, estado=None, token=None, estadoToken=None, nombre=None, apeCompleto=None, fechaNac=None, documento=None, tipo_documento_id = None, sexo=None, direccion=None, telefono=None, foto=None, rolId=None):
        self.id = id
        self.nombreUsuario = nombreUsuario
        self.email = email
        self.contrasena = contrasena
        self.estado = estado
        self.token = token
        self.estadoToken = estadoToken
        self.nombre = nombre
        self.apeCompleto = apeCompleto
        self.fechaNac = fechaNac
        self.documento = documento
        self.tipo_documento_id = tipo_documento_id
        self.sexo = sexo
        self.direccion = direccion
        self.telefono = telefono
        self.foto = foto
        self.rolId = rolId

    def agregar(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO usuario(nombre_usuario, email, contrasena, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            con.autocommit = False
            direccion = self.direccion if self.direccion is not None else ""
            telefono = self.telefono if self.telefono is not None else ""
            foto = self.foto if self.foto is not None else ""
            cursor.execute(sql, [self.nombreUsuario, self.email, self.contrasena, self.estado, self.token, self.estadoToken, self.nombre, self.apeCompleto, self.fechaNac, self.documento, self.tipo_documento_id, self.sexo, direccion, telefono, foto, self.rolId])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        return json.dumps({'status': True, 'data': {'usuario_id': self.id}, 'message': "Usuario agregado correctamente"})

    def actualizar(self):
        con = db().open
        cursor = con.cursor()
        sql = "UPDATE usuario SET nombre_usuario = %s, email = %s,  estado = %s, token = %s, estado_token = %s, nombre = %s, ape_completo = %s, fecha_nac = %s, documento = %s, sexo = %s, direccion = %s, telefono = %s, foto = %s, rol_id = %s WHERE id = %s"
        try:
            con.autocommit = False
            direccion = self.direccion if self.direccion is not None else ""
            telefono = self.telefono if self.telefono is not None else ""
            foto = self.foto if self.foto is not None else ""
            cursor.execute(sql, [self.nombreUsuario, self.email, self.estado, self.token, self.estadoToken, self.nombre, self.apeCompleto, self.fechaNac, self.documento, self.sexo, direccion, telefono, foto, self.rolId, self.id])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        return json.dumps({'status': True, 'data': {'usuario_id': self.id}, 'message': "Usuario actualizado correctamente"})

    def eliminar(self):
        con = db().open
        cursor = con.cursor()
        sql = "update usuario set estado = '0' where id = %s"
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
        return json.dumps({'status': True, 'data': {'usuario_id': self.id}, 'message': "Usuario actualizado correctamente"})

    def listar_usuarios(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre_usuario, email, nombre, ape_completo, fecha_nac, documento, sexo, direccion, telefono, foto, rol_id FROM usuario WHERE estado = '1' ORDER BY nombre_usuario;"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        cursor.close()
        con.close()
        
        # Convertir objetos de tipo date a string
        usuarios_list = []
        for usuario in usuarios:
            usuario_dict = dict(usuario)
            if isinstance(usuario_dict.get('fecha_nac'), date):
                usuario_dict['fecha_nac'] = usuario_dict['fecha_nac'].strftime('%Y-%m-%d')
            usuarios_list.append(usuario_dict)
        
        if usuarios_list:
            return json.dumps({'status': True, 'data': usuarios_list, 'message': 'Lista de usuarios'})
        else:
            return json.dumps({'status': True, 'data': [], 'message': 'No hay usuarios registrados'})
        
        
    def cambiar_contrasena(self, nueva_contrasena):
        try:
            con = db().open
            cursor = con.cursor()
            query = "UPDATE usuario SET contrasena = %s WHERE id = %s"
            values = (nueva_contrasena, self.id)
            cursor.execute(query, values)
            con.commit()
            return json.dumps({'status': True, 'message': 'Contraseña actualizada correctamente'})
        except Exception as e:
            return json.dumps({'status': False, 'message': str(e)})
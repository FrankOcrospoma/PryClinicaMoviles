from bd import Conexion as db
import json
from datetime import date
from util import CustomJsonEncoder

class Usuario():
    def __init__(self, id=None, nombre_usuario=None, email=None, contrasena=None, estado=None, token=None, estado_token=None, nombre=None, ape_completo=None, fecha_nac=None, documento=None, tipo_documento_id=None, sexo=None, direccion=None, telefono=None, foto=None, rol_id=None):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena = contrasena
        self.estado = estado
        self.token = token
        self.estado_token = estado_token
        self.nombre = nombre
        self.ape_completo = ape_completo
        self.fecha_nac = fecha_nac
        self.documento = documento
        self.tipo_documento_id = tipo_documento_id
        self.sexo = sexo
        self.direccion = direccion
        self.telefono = telefono
        self.foto = foto
        self.rol_id = rol_id

    def agregar(self):
        con = db().open
        cursor = con.cursor()
        sql = "INSERT INTO usuario(nombre_usuario, email, contrasena, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            con.autocommit = False
            direccion = self.direccion if self.direccion is not None else ""
            telefono = self.telefono if self.telefono is not None else ""
            foto = self.foto if self.foto is not None else ""
            cursor.execute(sql, [self.nombre_usuario, self.email, self.contrasena, self.estado, self.token, self.estado_token, self.nombre, self.ape_completo, self.fecha_nac, self.documento, self.tipo_documento_id, self.sexo, direccion, telefono, foto, self.rol_id])
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
            cursor.execute(sql, [self.nombre_usuario, self.email, self.estado, self.token, self.estado_token, self.nombre, self.ape_completo, self.fecha_nac, self.documento, self.sexo, direccion, telefono, foto, self.rol_id, self.id])
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
        
    # Método para guardar el código de recuperación
    def guardar_codigo_recuperacion(self, codigo_recuperacion):
        con = db().open
        cursor = con.cursor()
        sql = "UPDATE usuario SET codigo_recuperacion = %s WHERE email = %s"
        try:
            con.autocommit = False
            cursor.execute(sql, [codigo_recuperacion, self.email])
            con.commit()
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()
        return json.dumps({'status': True, 'data': None, 'message': "Código de recuperación guardado correctamente"})

    # Otros métodos de la clase...

    @staticmethod
    def buscar_por_email(email):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre_usuario, email, nombre, ape_completo, fecha_nac, documento, sexo, direccion, telefono, foto, rol_id FROM usuario WHERE email = %s AND estado = '1'"
        cursor.execute(sql, [email])
        usuario_data = cursor.fetchone()
        cursor.close()
        con.close()

        if usuario_data:
            # Verificar si usuario_data es un diccionario y contiene todas las claves esperadas
            required_keys = ['id', 'nombre_usuario', 'email', 'contrasena', 'estado', 'token', 'estado_token', 'nombre', 'ape_completo', 'fecha_nac', 'documento', 'tipo_documento_id', 'sexo', 'direccion', 'telefono', 'foto', 'rol_id']
            for key in required_keys:
                if key not in usuario_data:
                    usuario_data[key] = None  # Establecer a None si la clave no existe

            usuario_data_dict = {
                'id': usuario_data['id'],
                'nombre_usuario': usuario_data['nombre_usuario'],
                'email': usuario_data['email'],
                'contrasena': usuario_data['contrasena'],
                'estado': usuario_data['estado'],
                'token': usuario_data['token'],
                'estado_token': usuario_data['estado_token'],
                'nombre': usuario_data['nombre'],
                'ape_completo': usuario_data['ape_completo'],
                'fecha_nac': usuario_data['fecha_nac'],
                'documento': usuario_data['documento'],
                'tipo_documento_id': usuario_data['tipo_documento_id'],
                'sexo': usuario_data['sexo'],
                'direccion': usuario_data['direccion'],
                'telefono': usuario_data['telefono'],
                'foto': usuario_data['foto'],
                'rol_id': usuario_data['rol_id']
            }
            return Usuario(**usuario_data_dict)
        else:
            return None

    def verificar_codigo(self, codigo):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT codigo_recuperacion FROM usuario WHERE email = %s AND codigo_recuperacion = %s"
        cursor.execute(sql, [self.email, codigo])
        result = cursor.fetchone()
        cursor.close()
        con.close()

        if result:
            return True
        else:
            return False

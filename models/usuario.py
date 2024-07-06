from bd import Conexion as db
import json
from datetime import date
from util import CustomJsonEncoder
from datetime import datetime

class Usuario():
    def __init__(self, id=None, nombre_usuario=None, email=None, contrasena=None, estado=None, token=None, estado_token=None, nombre=None, ape_completo=None, fecha_nac=None, documento=None, tipo_documento_id=None, sexo=None, direccion=None, telefono=None, foto=None, rol_id=None, notificacion=None):
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
        self.notificacion = notificacion

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
        sql = "UPDATE usuario SET nombre_usuario = %s, email = %s, estado = %s, token = %s, estado_token = %s, nombre = %s, ape_completo = %s, fecha_nac = %s, documento = %s, sexo = %s, direccion = %s, telefono = %s, foto = %s, rol_id = %s WHERE id = %s"
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


#Anyelo
    def actualizar_estado_aea(self, usuario_id, notificacion):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET notificacion = %s WHERE id = %s
            """
            cursor.execute(sql, (notificacion, usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})
    
    
    def bloquear_usuario_guzman(self, usuario_id):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET estado = 0 WHERE id = %s
            """
            cursor.execute(sql, ( usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Usuario bloqueado por limite de intentos'})




# #Anyelo
#     def actualizar_estado_aea(self, notificacion_id, estado):
#         con = db().open
#         cursor = con.cursor()

#         try:
#             sql = """
#             UPDATE notificacion SET leida = %s WHERE id = %s
#             """
#             cursor.execute(sql, (estado, notificacion_id))
#             con.commit()

#         except con.Error as error:  
#             con.rollback()
#             return json.dumps({'status': False, 'data': None, 'message': str(error)})

#         finally:
#             cursor.close()
#             con.close()

#         return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})


    def listar_usuarios_pacientes(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre_usuario, email, nombre, ape_completo, fecha_nac, documento, sexo, direccion, telefono, foto, rol_id FROM usuario WHERE estado = '1' and rol_id = 2 ORDER BY nombre_usuario;"
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
    def listar_usuarios_odontologos(self):
        con = db().open
        cursor = con.cursor()
        sql = "SELECT id, nombre_usuario, email, nombre, ape_completo, fecha_nac, documento, sexo, direccion, telefono, foto, rol_id FROM usuario WHERE estado = '1' and rol_id = 3 ORDER BY nombre_usuario;"
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

    @staticmethod
    def buscar_por_email(email):
        con = db().open
        cursor = con.cursor()
        sql = """
            SELECT id, nombre_usuario, email, contrasena, estado, token, estado_token, nombre, ape_completo, 
                   fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id
            FROM usuario 
            WHERE email = %s AND estado = '1'
        """
        cursor.execute(sql, [email])
        usuario_data = cursor.fetchone()
        cursor.close()
        con.close()

        if usuario_data:
            print(usuario_data)  # Depuración para verificar la estructura de usuario_data
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



#paciente 

    def agregar_paciente(self):
        con = db().open
        cursor = con.cursor()

        try:
            cursor.execute("SELECT id, nombre FROM rol WHERE nombre = 'paciente';")
            rol = cursor.fetchone()
            if rol is None:
                raise Exception("Rol 'paciente' no encontrado")

            rol_id = rol["id"]

            sql = """
            INSERT INTO usuario (
                estado_token, nombre_usuario, email, contrasena, estado, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, rol_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            con.autocommit = False
            direccion = self.direccion if self.direccion is not None else ""
            telefono = self.telefono if self.telefono is not None else ""

            cursor.execute(sql, [
                self.estado_token, self.nombre_usuario, self.email, self.contrasena, self.estado, self.nombre, self.ape_completo,
                self.fecha_nac, self.documento, self.tipo_documento_id, self.sexo, direccion, telefono, rol_id
            ])
            con.commit()
            paciente_id = cursor.lastrowid

            return json.dumps({'status': True, 'data': {'usuario_id': paciente_id}, 'message': "Paciente agregado correctamente"})
        except Exception as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': f"Error: {str(error)}"})
        finally:
            cursor.close()
            con.close()

#Odontologo
    def agregar_odontologo(self):
        con = db().open
        cursor = con.cursor()

        try:
            cursor.execute("SELECT id, nombre FROM rol WHERE nombre = 'odontologo';")
            rol = cursor.fetchone()
            if rol is None:
                raise Exception("Rol 'Odontologo' no encontrado")

            rol_id = rol["id"]

            sql = """
            INSERT INTO usuario (
                estado_token, nombre_usuario, email, contrasena, estado, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, rol_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            con.autocommit = False
            direccion = self.direccion if self.direccion is not None else ""
            telefono = self.telefono if self.telefono is not None else ""

            cursor.execute(sql, [
                self.estado_token, self.nombre_usuario, self.email, self.contrasena, self.estado, self.nombre, self.ape_completo,
                self.fecha_nac, self.documento, self.tipo_documento_id, self.sexo, direccion, telefono, rol_id
            ])
            con.commit()
            paciente_id = cursor.lastrowid

            return json.dumps({'status': True, 'data': {'usuario_id': paciente_id}, 'message': "Odontologo agregado correctamente"})
        except Exception as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': f"Error: {str(error)}"})
        finally:
            cursor.close()
            con.close()


    def notificar_paciente(self, data):
        con = db().open
        cursor = con.cursor()
        try:
            
            sql_paciente = """
                SELECT notificacion FROM usuario
                WHERE id = %s
            """
            cursor.execute(sql_paciente, (data["paciente_id"], ))
            usario_estado_noti = cursor.fetchone()
            
            numero = 0
            for usu in usario_estado_noti:
                print (usu.get('notificacion'))
                numero = usu.get('notificacion')
            if numero == 1:
            

                sql = """
                INSERT INTO notificacion (
                    usuario_id, mensaje, fecha, leida
                ) VALUES (
                    %s, %s, %s, %s
                )
                """

                con.autocommit = False

                cursor.execute(sql, [data["paciente_id"], data["mensaje"], datetime.now(), data["leida"]])
                con.commit()

                return json.dumps({'status': True, 'data': None, 'message': "Notificacion  agregado correctamente"})
            else:
                return json.dumps({'status': True, 'data': None, 'message': "El usuario no desea recibir notificaciones",  })
                
        except Exception as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': f"Error: {str(error)}"})
        finally:
            cursor.close()
            con.close()


    def lista_notificaciones_paciente(self, paciente_id):
        con = db().open
        cursor = con.cursor()
        try:
            sql = """
            SELECT 
                n.id AS notificacion_id, 
                n.mensaje, 
                n.fecha, 
                case n.leida
                    when 0 then 'No leído'
                    else 'Leído'
                END AS estado
            FROM notificacion n
            INNER JOIN usuario u ON u.id=n.usuario_id
            WHERE u.id = %s AND u.notificacion = 1
            """
            cursor.execute(sql, [paciente_id])

            data = cursor.fetchall()


            for x in data:
                fecha = str(x["fecha"])
                print(fecha)
                x['fecha'] = fecha


            return json.dumps({'status': True, 'data': data, 'message': "Listado de Notificacion correctamente"})
        except Exception as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': f"Error: {str(error)}"})
        finally:
            cursor.close()
            con.close()

    def actualizar_estado_notificacion_geancarlos(self, usuario_id, estado):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET notificacion = %s WHERE id = %s
            """
            cursor.execute(sql, (estado, usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})

#Anyelo
    def actualizar_estado_bloqueado(self, usuario_id, bloqueado):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET bloqueado = %s WHERE id = %s
            """
            cursor.execute(sql, (bloqueado, usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})


    def actualizar_estado_notificacion(self, usuario_id, notificacion):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET notificacion = %s WHERE id = %s
            """
            cursor.execute(sql, (notificacion, usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación del usuario actualizado correctamente'})


    def cambiar_estado_notificacion_por_paciente(self, paciente_id, notificacion):
        con = db().open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET notificacion=%s WHERE id = %s;
                        """
            cursor.execute(sql, (notificacion, paciente_id))
            
            con.commit()
            return json.dumps({'status': True, 'data': {'paciente_id': paciente_id}, 'message': 'Notificación actualizado correctamente'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()



    def actualizar_estado_noti_guzman(self, usuario_id, estado):
        con = db.open
        cursor = con.cursor()

        try:
            sql = """
            UPDATE usuario SET notificacion = %s WHERE id = %s
            """
            cursor.execute(sql, (estado, usuario_id))
            con.commit()

        except con.Error as error:  
            con.rollback()
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

        return json.dumps({'status': True, 'message': 'Estado de la notificación actualizado correctamente'})







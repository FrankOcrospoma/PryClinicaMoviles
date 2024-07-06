from bd import Conexion as db
import json
from datetime import date

class Sesion:
    def __init__(self, email=None, clave=None):
        self.email = email
        self.clave = clave
    
    #Anyelo
    def iniciarSesion(self):
        # Abrir la conexion
        con = db().open
        
        # Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        # Preparar la consulta sql para validar las credenciales
        sql = """
            SELECT * 
            FROM usuario
            WHERE email = %s
        """    
        
        # Ejecutar la consulta sql 
        cursor.execute(sql, [self.email])
        
        # Almacenar el resultado de la consulta
        datos = cursor.fetchone()
        
        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()
        
        # Retornar el resultado del método
        if datos: # Validar si hay datos
            if datos['estado'] == 1: # Estado '1' = activo
                if datos['bloqueado'] >= 3:
                    return json.dumps({'status': False, 'data': None, 'message': "Cuenta bloqueada"})

                if datos['contrasena'] == self.clave:
                    # Resetear intentos fallidos
                    self.resetearIntentosFallidos(datos['id'])
                    datos_serializables = self.convertir_a_serializable(datos)
                    return json.dumps({'status': True, 'data': datos_serializables, 'message': 'Credenciales correctas'})
                else:
                    # Incrementar intentos fallidos
                    self.incrementarIntentosFallidos(datos['id'])
                    return json.dumps({'status': False, 'data': None, 'message': "Credenciales incorrectas"})
            else:
                return json.dumps({'status': False, 'data': datos['nombre_usuario'], 'message': "Cuenta inactiva"})
        else: 
            return json.dumps({'status': False, 'data': None, 'message': "Credenciales incorrectas"})

    #Anyelo
    def incrementarIntentosFallidos(self, user_id):
        con = db().open
        cursor = con.cursor()
        
        sql = """
            UPDATE usuario
            SET bloqueado = bloqueado + 1
            WHERE id = %s
        """
        
        cursor.execute(sql, [user_id])
        con.commit()
        cursor.close()
        con.close()

    #Anyelo
    def resetearIntentosFallidos(self, usuario_id):
        con = db().open
        cursor = con.cursor()
        
        sql = """
            UPDATE usuario
            SET bloqueado = 0
            WHERE id = %s
        """
        
        cursor.execute(sql, [usuario_id])
        con.commit()
        cursor.close()
        con.close()



    def iniciarSesionAdmin(self):
        # Abrir la conexion
        con = db().open
        
        # Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        # Preparar la consulta sql para validar las credenciales
        sql = """
            SELECT * 
            FROM usuario
            WHERE email = %s
            AND contrasena = %s
            AND rol_id = 1
        """    
        
        # Ejecutar la consulta sql 
        cursor.execute(sql, [self.email, self.clave])
        
        # Almacenar el resultado de la consulta
        datos = cursor.fetchone()
        
        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()
        
        # Retornar el resultado del método
        if datos: # Validar si hay datos
            print(datos)
            if datos['estado'] == 1: # Estado '1' = activo
                # Convertir datos a un formato serializable
                datos_serializables = self.convertir_a_serializable(datos)
                return json.dumps({'status': True, 'data': datos_serializables, 'message': 'Credenciales correctas'})
            else:
                return json.dumps({'status': False, 'data': datos['nombre_usuario'], 'message': "Cuenta inactiva"})
        else: # Si no hay datos: Credenciales son incorrectas, el usuario no existe
            return json.dumps({'status': False, 'data': None, 'message': "Credenciales incorrectas"})

    def convertir_a_serializable(self, datos):
        # Convertir objetos datetime.date a cadena
        datos_serializables = {}
        for key, value in datos.items():
            if isinstance(value, date):
                datos_serializables[key] = value.isoformat()
            else:
                datos_serializables[key] = value
        return datos_serializables
  
    def actualizarToken(self, token, usuarioID):
        # Abrir la conexion
        con = db().open
        
        # Crear un cursor que devuelve la consulta sql
        cursor = con.cursor()
        
        # Preparar la sentencia de actualización
        sql = "UPDATE usuario SET token = %s, estado_token = '1' WHERE id = %s"
        
        try:
            # Iniciar la actualización, indicando que la operación (Transacción)
            # Se confirma de manera manual
            con.autocommit = False
            
            # Ejecutar la sentencia
            cursor.execute(sql, [token, usuarioID])
            # Confirmar la actualización
            con.commit()
            
        except con.Error as error:  
            # Revocar la actualización
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': None, 'message': None})
   
    def validarEstadoToken(self, usuarioID):
        # Abrir una conexión a la BD
        con = db().open

        # Crear un cursor para almacenar los datos que devuelve la consulta SQL
        cursor = con.cursor()

        # Preparar la consulta SQL para validar las credenciales
        sql = "SELECT estado_token FROM usuario WHERE id = %s"
        
        # Ejecutar la consulta SQL
        cursor.execute(sql, [usuarioID])

        # Almacenar los datos que devuelve la consulta SQL
        datos = cursor.fetchone()

        # Cerrar el cursor y la conexión a la BD
        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos, 'message': 'Estado de token'})
        else:
            return json.dumps({'status': False, 'data': None, 'message': 'Estado de token no encontrado'})

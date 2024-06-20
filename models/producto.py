from bd import Conexion as db
import json
from util import CustomJsonEncoder
import os
import base64
class Producto():
    def __init__(self, id=None, nombre=None, precio=None, categoriaId=None, foto=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoriaID = categoriaId
        self.foto = foto
    def catalago(self, productoID, almacenID):
       con = db().open
       
       cursor = con.cursor() 
       
       sql = """
       SELECT 
            p.id,
            p.nombre,
            p.precio, 
            c.nombre as categoria ,
            CONCAT('/static/imgs-producto/', p.id, '.jpg') AS foto,
            s.stock
        FROM producto p
            INNER JOIN categoria c ON c.id = p.categoria_id
            INNER JOIN stock_almacen s on (p.id = s.producto_id)  
        WHERE
            (case when %s = 0 then TRUE else p.id = %s end)	
            and s.almacen_id = %s
            and p.eliminado= '0'
        ORDER BY 
		    2
       """
       
       cursor.execute(sql, [productoID,productoID,almacenID])
       #Recuperar los datos de la consulta SQL
       datos = cursor.fetchall()
       
       #Cerrar el cursor y la conexion
       cursor.close()
       con.close()
       
       #Retornar los datos
       if datos:
           return json.dumps({'status':True, 'data': datos, 'message': 'catalago de productos'}, cls=CustomJsonEncoder )
       else:
            return json.dumps({'status':True, 'data': datos, 'message': 'sin registros'})

    def actualizar(self):
        #Abrir la conexion
        con = db().open
        
        #Crear un cursor que devuelve la conuslta sql
        cursor = con.cursor()
        
        #Prepar la sentencia de actualziacion
        sql = "Update PRODUCTO set nombre = %s, precio = %s, categoria_id = %s where id = %s"
        
        try:
            #Iniciar la actualizacion, indicando que la operacion (Transaccion)
            #Se confirma de manera manual
            con.autocommit = False
            #Ejecutar la sentencia
            cursor.execute(sql, [self.nombre, self.precio, self.categoriaID, self.id])
            
            #Cargar la foto del producto
            self.cargar_foto(self.foto, self.id)

            #Confirmar la operacion de agregar
            con.commit()
            
        except con.Error as error:  
            #Revocar la operacion de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'producto_id': self.id}, 'message': 'Producto actualizado correctamente'})

    def agregar(self):
        #Abrir la conexion
        con = db().open
        
        #Crear un cursor que devuelve la conuslta sql
        cursor = con.cursor()
        
        #Prepar la sentencia de actualziacion
        sql = "INSERT INTO PRODUCTO(nombre, precio, categoria_id) values(%s, %s, %s)"
        
        try:
            #Iniciar la actualizacion, indicando que la operacion (Transaccion)
            #Se confirma de manera manual
            con.autocommit = False
            #Ejecutar la sentencia
            cursor.execute(sql, [self.nombre, self.precio, self.categoriaID])
            self.id = con.insert_id()
            
            #Cargar la foto del producto
            self.cargar_foto(self.foto, self.id)

            #Confirmar la operacion de agregar
            con.commit()
            
        except con.Error as error:  
            #Revocar la operacion de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'producto_id': self.id}, 'message': 'Producto agregado correctamente'})

    def eliminar(self):
        #Abrir la conexion
        con = db().open
        
        #Crear un cursor que devuelve la conuslta sql
        cursor = con.cursor()
        
        #Prepar la sentencia de actualziacion
        sql = "Update PRODUCTO set eliminado = '1' where id = %s"
        
        try:
            #Iniciar la actualizacion, indicando que la operacion (Transaccion)
            #Se confirma de manera manual
            con.autocommit = False
            #Ejecutar la sentencia
            cursor.execute(sql, [self.id])

            #Confirmar la operacion de agregar
            con.commit()
            
        except con.Error as error:  
            #Revocar la operacion de agregar
            con.rollback()
            
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        return json.dumps({'status': True, 'data': {'producto_id': self.id}, 'message': 'Producto eliminado correctamente'})

    def cargar_foto(self, foto, id):
        #Cargar la foto del producto dentro de la carpeta static\imgs-producto
        #Decodificar la imagen del prodructo que viene en BASE64
        foto_bytes = base64.b64decode(foto)
        
        #Guardar la foto
        nombre_foto = str(id) + ".jpg"
        ruta_foto = os.path.join('static\imgs-producto', nombre_foto)
        with open(ruta_foto, 'wb') as archivo:
            archivo.write(foto_bytes)
        
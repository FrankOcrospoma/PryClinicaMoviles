from flask import Blueprint, request, jsonify
from models.sesion import Sesion
import json
import jwt
import datetime
from  config import SecretKey
#Generar un modulo para gestionar las sesiones de usuario
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear el "end point" para validar la sesion del usuario


@ws_sesion.route('/login', methods=['POST'])    
def login():
    if request.method == 'POST':
        if 'email' not in request.form or 'clave' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': "Falta parámetros"}), 400
        
        #Si los parametros si son enviados, entonces corresponde recoger los datos
        email = request.form['email']
        clave = request.form['clave']
        
        #Instanciar a la clase sesion, la cual me permite validar las credenciales del usuario
        obj = Sesion(email, clave)
        
        #Ejecutar el metodo InciarSesion()
        resultadoJSONstring = obj.iniciarSesion()
        
        #Convertir el objeto "json string" a "json object"
        resultadoJSONobject = json.loads(resultadoJSONstring)
        
        #Mostrar los resultados
        if resultadoJSONobject['status'] == True:
            #almacenar el id del usario que ha iniado sesion en una variable
            usuarioID = resultadoJSONobject['data']['id']
            
            #generar el token con jwt, almacenado dentro de la data el id del usuario
            token = jwt.encode({'usuarioID': usuarioID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)}, SecretKey.JWT_SECRET_KEY )
            
            #incorporar la variable token el resultado del servicio 
            resultadoJSONobject['data']['token']=token

            #Actualizar el token del usuario en la bd
            resultadoActualizacionJSONobject =json.loads(obj.actualizarToken(token, usuarioID)) 
            
            if resultadoActualizacionJSONobject['status'] == False:
                return jsonify(resultadoActualizacionJSONobject), 500
            
            #imprimir el resultado en JSON
            return jsonify(resultadoJSONobject), 200 # 200 es de ok
        else:
            return jsonify(resultadoJSONobject), 401 # 401 es de no autorizado
        
        
        

@ws_sesion.route('/loginAdmin', methods=['POST'])    
def login():
    if request.method == 'POST':
        if 'email' not in request.form or 'clave' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': "Falta parámetros"}), 400
        
        #Si los parametros si son enviados, entonces corresponde recoger los datos
        email = request.form['email']
        clave = request.form['clave']
        
        #Instanciar a la clase sesion, la cual me permite validar las credenciales del usuario
        obj = Sesion(email, clave)
        
        #Ejecutar el metodo InciarSesion()
        resultadoJSONstring = obj.iniciarSesionAdmin()
        
        #Convertir el objeto "json string" a "json object"
        resultadoJSONobject = json.loads(resultadoJSONstring)
        
        #Mostrar los resultados
        if resultadoJSONobject['status'] == True:
            #almacenar el id del usario que ha iniado sesion en una variable
            usuarioID = resultadoJSONobject['data']['id']
            
            #generar el token con jwt, almacenado dentro de la data el id del usuario
            token = jwt.encode({'usuarioID': usuarioID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)}, SecretKey.JWT_SECRET_KEY )
            
            #incorporar la variable token el resultado del servicio 
            resultadoJSONobject['data']['token']=token

            #Actualizar el token del usuario en la bd
            resultadoActualizacionJSONobject =json.loads(obj.actualizarToken(token, usuarioID)) 
            
            if resultadoActualizacionJSONobject['status'] == False:
                return jsonify(resultadoActualizacionJSONobject), 500
            
            #imprimir el resultado en JSON
            return jsonify(resultadoJSONobject), 200 # 200 es de ok
        else:
            return jsonify(resultadoJSONobject), 401 # 401 es de no autorizado
        
from flask import Blueprint, request, jsonify
from models.producto import Producto
import json
import validarToken as vt

#Generar un modulo para gestionar el producto
ws_producto = Blueprint('ws_producto', __name__)

@ws_producto.route('/producto/catalago/<int:id>/<int:almacen_id>', methods=['GET'])
@vt.validar
def catalago(id, almacen_id):
    if request.method == 'GET':
        if not id:
            if id != 0:
                return jsonify({'status': False, 'data': None, 'message': 'Falta el id del producto'}), 400
        if not almacen_id:
                return jsonify({'status': False, 'data': None, 'message': 'Falta el id del almacen'}), 400
        
        obj = Producto()
        resultadoCatalogoJSONObject = json.loads(obj.catalago(id, almacen_id))
        
        if resultadoCatalogoJSONObject['status'] == True:
            return jsonify(resultadoCatalogoJSONObject), 200 #ok
        else:
            return jsonify(resultadoCatalogoJSONObject), 204 #no content

@ws_producto.route('/producto/agregar', methods=['POST'])
@vt.validar
def agregar_producto():
    if request.method == 'POST':
        #Validar los parametros de entrada
        if 'nombre' not in request.form or 'precio' not in request.form or 'categoria_id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400
        
        #leer los parametros de entrada
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']
        foto = request.form['foto'] 
        #Instanciar el objeto de la clase Producto       
        obj = Producto(0, nombre, precio, categoria_id, foto)
        
        #Ejecutar el metodo agregar
        resultadoAgregarJSONObject = json.loads(obj.agregar())
        
        if resultadoAgregarJSONObject['status'] == True:
            
            
            return jsonify(resultadoAgregarJSONObject), 200 #ok
        else:
            return jsonify(resultadoAgregarJSONObject), 500 #no content


@ws_producto.route('/producto/actualizar', methods=['PUT'])
@vt.validar
def actualizar_producto():
    if request.method == 'PUT':
        #Validar los parametros de entrada
        if {'nombre', 'precio', 'categoria_id', 'id'} - set(request.form.keys()):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400
        
        #leer los parametros de entrada
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']
        foto = request.form['foto'] 
        id = request.form['id']
        #Instanciar el objeto de la clase Producto       
        obj = Producto(id, nombre, precio, categoria_id, foto)
        
        #Ejecutar el metodo agregar
        resultadoAgregarJSONObject = json.loads(obj.actualizar())
        
        if resultadoAgregarJSONObject['status'] == True:
            
            
            return jsonify(resultadoAgregarJSONObject), 200 #ok
        else:
            return jsonify(resultadoAgregarJSONObject), 500 #no content


@ws_producto.route('/producto/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_producto():
    if request.method == 'DELETE':
        #Validar los parametros de entrada
        if {'id'} - set(request.form.keys()):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400
        

        id = request.form['id']
        #Instanciar el objeto de la clase Producto       
        obj = Producto(id, None, None, None, None)
        
        #Ejecutar el metodo agregar
        resultadoAgregarJSONObject = json.loads(obj.eliminar())
        
        if resultadoAgregarJSONObject['status'] == True:
            
            
            return jsonify(resultadoAgregarJSONObject), 200 #ok
        else:
            return jsonify(resultadoAgregarJSONObject), 500 #no content

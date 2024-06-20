from flask import Blueprint, request, jsonify
from models.rol import Rol
import json
import validarToken as vt

ws_rol = Blueprint('ws_rol', __name__)

@ws_rol.route('/rol', methods=['GET'])
@vt.validar
def listar_roles():
  if request.method == 'GET':
    obj = Rol()
    resultado_roles = json.loads(obj.listar_roles())
    
    return jsonify(resultado_roles), 200

@ws_rol.route('/rol/agregar', methods=['POST'])
@vt.validar
def agregar_rol():
  if request.method == 'POST':
    if 'nombre' not in request.form:
      return jsonify({'status': False, 'data': None, 'message': 'Falta el nombre del rol'}), 400


    nombre = request.form['nombre']
    obj = Rol(None, nombre)
    resultado_agregar_rol = json.loads(obj.agregar_rol())
    return jsonify(resultado_agregar_rol), 200

@ws_rol.route('/rol/actualizar', methods=['PUT'])
@vt.validar
def actualizar_rol():
  if request.method == 'PUT':
    if {'id', 'nombre'} - set(request.form.keys()):
      return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

    id = request.form['id']
    nombre = request.form['nombre']
    obj = Rol(id, nombre)
    resultado_actualizar_rol = json.loads(obj.actualizar_rol())
    
    return jsonify(resultado_actualizar_rol), 200

@ws_rol.route('/rol/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_rol():
  if request.method == 'DELETE':
    if 'id' not in request.form:
      return jsonify({'status': False, 'data': None, 'message': 'Falta el ID del rol'}), 400
    id = request.form['id']
    obj = Rol(id)
    resultado_eliminar_rol = json.loads(obj.eliminar_rol())

    return jsonify(resultado_eliminar_rol), 200

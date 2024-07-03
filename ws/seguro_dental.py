from flask import Blueprint, request, jsonify
from models.seguro_dental import SeguroDental
import json
import validarToken as vt

# Generar un módulo para gestionar seguros dentales
ws_seguro_dental = Blueprint('ws_seguro_dental', __name__)

@ws_seguro_dental.route('/seguro-dental/<int:id>', methods=['GET'])
#@vt.validar
def obtener_seguro_dental(id):
  if request.method == 'GET':

    obj = SeguroDental()
    resultado_obtener_seguro = json.loads(obj.obtener_seguro_dental(id))
    
    if resultado_obtener_seguro['status'] == True:
      return jsonify(resultado_obtener_seguro), 200 #ok
    else:
      return jsonify(resultado_obtener_seguro), 200 #ok
    
@ws_seguro_dental.route('/seguro-dental/agregar', methods=['POST'])
#@vt.validar
def agregar_seguro_dental():
  if request.method == 'POST':
    if {'nombre_compania', 'tipo_cobertura', 'telefono_compania', 'paciente_id'} - set(request.form.keys()):
      return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
      
    nombre_compania = request.form['nombre_compania']
    tipo_cobertura = request.form['tipo_cobertura']
    telefono_compania = request.form['telefono_compania']
    paciente_id = request.form['paciente_id']

    obj = SeguroDental(None, nombre_compania, tipo_cobertura, telefono_compania, paciente_id)
    resultado_agregar_seguro = json.loads(obj.agregar_seguro())

    if resultado_agregar_seguro['status'] == True:
      return jsonify(resultado_agregar_seguro), 200 #ok
    else:
      return jsonify(resultado_agregar_seguro), 200 #ok   

@ws_seguro_dental.route('/seguro-dental/actualizar', methods=['PUT'])
#@vt.validar
def actualizar_seguro_dental():
  if request.method == 'PUT':
    if {'id', 'nombre_compania', 'tipo_cobertura', 'telefono_compania'} - set(request.form.keys()):
      return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

    id = request.form['id']
    nombre_compania = request.form['nombre_compania']
    tipo_cobertura = request.form['tipo_cobertura']
    telefono_compania = request.form['telefono_compania']

    obj = SeguroDental(id, nombre_compania, tipo_cobertura, telefono_compania)

    resultado_actualizar_seguro = json.loads(obj.actualizar_seguro())

    if resultado_actualizar_seguro['status'] == True:
      return jsonify(resultado_actualizar_seguro), 200 #ok
    else:
      return jsonify(resultado_actualizar_seguro), 200 #ok

@ws_seguro_dental.route('/seguro-dental/eliminar', methods=['DELETE'])
#@vt.validar
def eliminar_seguro_dental():
  if request.method == 'DELETE':
    if 'id' not in request.args:
      return jsonify({'status': False, 'data': None, 'message': 'Falta el ID del seguro dental'}), 400

    id = request.args.get('id')

    obj = SeguroDental(id)

    resultado_eliminar_seguro = json.loads(obj.eliminar_seguro())

    if resultado_eliminar_seguro['status'] == True:
      return jsonify(resultado_eliminar_seguro), 200 #ok
    else:
      return jsonify(resultado_eliminar_seguro), 200 #ok

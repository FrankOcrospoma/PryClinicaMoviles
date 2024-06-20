from flask import Blueprint, request, jsonify
from models.DetalleEspecialidad import DetalleEspecialidad
import json
ws_detalle_especialidad = Blueprint('ws_detalle_especialidad', __name__)

@ws_detalle_especialidad.route('/detalle_especialidad/lista', methods=['GET'])
def lista_detalles():
    obj = DetalleEspecialidad()
    return jsonify(json.loads(obj.listar_detalles())), 200

@ws_detalle_especialidad.route('/detalle_especialidad/agregar', methods=['POST'])
def agregar_detalle():
    odontologo_id = request.form['odontologo_id']
    especialidad_id = request.form['especialidad_id']
    obj = DetalleEspecialidad(odontologo_id, especialidad_id)
    return jsonify(json.loads(obj.agregar_detalle())), 200

@ws_detalle_especialidad.route('/detalle_especialidad/eliminar', methods=['DELETE'])
def eliminar_detalle():
    odontologo_id = request.form['odontologo_id']
    especialidad_id = request.form['especialidad_id']
    obj = DetalleEspecialidad(odontologo_id, especialidad_id)
    return jsonify(json.loads(obj.eliminar_detalle())), 200

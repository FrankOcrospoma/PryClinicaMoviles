from flask import Blueprint, request, jsonify
from models.especialidad import Especialidad
import json
import validarToken as vt

# Generar un módulo para gestionar las especialidades
ws_especialidad = Blueprint('ws_especialidad', __name__)

@ws_especialidad.route('/especialidad/lista', methods=['GET'])
@vt.validar
def lista_especialidades():
    if request.method == 'GET':
        obj = Especialidad()
        return jsonify(json.loads(obj.listar_especialidades())), 200

@ws_especialidad.route('/especialidad/registrar', methods=['POST'])
@vt.validar
def registrar_especialidad():
    if request.method == 'POST':
        nombre = request.form['nombre']
        obj = Especialidad(None, nombre)
        return jsonify(json.loads(obj.registrar_especialidad())), 200

@ws_especialidad.route('/especialidad/actualizar', methods=['PUT'])
@vt.validar
def actualizar_especialidad():
    if request.method == 'PUT':
        id = request.form['id']
        nombre = request.form['nombre']
        obj = Especialidad(id, nombre)
        return jsonify(json.loads(obj.actualizar_especialidad())), 200

@ws_especialidad.route('/especialidad/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_especialidad():
    if request.method == 'DELETE':
        id = request.form['id']
        obj = Especialidad(id)
        return jsonify(json.loads(obj.eliminar_especialidad())), 200

from flask import Blueprint, request, jsonify
from models.tratamiento import Tratamiento
import json
import validarToken as vt

ws_tratamiento = Blueprint('ws_tratamiento', __name__)

@ws_tratamiento.route('/tratamiento/lista', methods=['GET'])
@vt.validar
def lista_tratamientos():
    if request.method == 'GET':
        obj = Tratamiento()
        return jsonify(json.loads(obj.listar_tratamientos())), 200

@ws_tratamiento.route('/tratamiento/registrar', methods=['POST'])
@vt.validar
def registrar_tratamiento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        obj = Tratamiento(None, nombre, descripcion, float(costo))
        return jsonify(json.loads(obj.registrar_tratamiento())), 200

@ws_tratamiento.route('/tratamiento/actualizar', methods=['PUT'])
@vt.validar
def actualizar_tratamiento():
    if request.method == 'PUT':
        id = request.form['id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        obj = Tratamiento(id, nombre, descripcion, float(costo))
        return jsonify(json.loads(obj.actualizar_tratamiento())), 200

@ws_tratamiento.route('/tratamiento/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_tratamiento():
    if request.method == 'DELETE':
        id = request.form['id']
        obj = Tratamiento(id)
        return jsonify(json.loads(obj.eliminar_tratamiento())), 200
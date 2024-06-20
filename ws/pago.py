from flask import Blueprint, request, jsonify
from models.pago import Pago
import json
import validarToken as vt

ws_pago = Blueprint('ws_pago', __name__)

@ws_pago.route('/pago/lista', methods=['GET'])
@vt.validar
def lista_pagos():
    if request.method == 'GET':
        obj = Pago()
        return jsonify(json.loads(obj.listar_pagos())), 200

@ws_pago.route('/pago/registrar', methods=['POST'])
@vt.validar
def registrar_pago():
    if request.method == 'POST':
        monto = request.form['monto']
        estado = request.form['estado']
        atencion_id = request.form['atencion_id']
        obj = Pago(None, float(monto), estado, int(atencion_id))
        return jsonify(json.loads(obj.registrar_pago())), 200

@ws_pago.route('/pago/actualizar', methods=['PUT'])
@vt.validar
def actualizar_pago():
    if request.method == 'PUT':
        id = request.form['id']
        monto = request.form['monto']
        estado = request.form['estado']
        atencion_id = request.form['atencion_id']
        obj = Pago(int(id), float(monto), estado, int(atencion_id))
        return jsonify(json.loads(obj.actualizar_pago())), 200

@ws_pago.route('/pago/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_pago():
    if request.method == 'DELETE':
        id = request.form['id']
        obj = Pago(int(id))
        return jsonify(json.loads(obj.eliminar_pago())), 200

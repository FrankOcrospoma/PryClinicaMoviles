import json
from flask import Blueprint, request, jsonify
from models.notificacion import Notificacion

ws_notificacion = Blueprint('ws_notificacion', __name__)

@ws_notificacion.route('/notificacion/registrar', methods=['POST'])
#@vt.validar
def registrar_notificacion():
    if request.method == 'POST':
        # Validar los parámetros de entrada necesarios para registrar una notificación
        required_fields = ['cita_id', 'mensaje']
        if not all(field in request.form for field in required_fields):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

        # Leer los parámetros de entrada
        cita_id = request.form['cita_id']
        mensaje = request.form['mensaje']

        # Instanciar el objeto de la clase Notificacion
        obj = Notificacion(cita_id, mensaje)
        
        # Ejecutar el método registrar
        resultadoAgregarJSONObject = json.loads(obj.registrar(cita_id))
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 # OK
        else:
            return jsonify(resultadoAgregarJSONObject), 500 # Internal Server Error

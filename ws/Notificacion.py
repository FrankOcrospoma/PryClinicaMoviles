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


        cita_id = request.form['cita_id']
        mensaje = request.form['mensaje']


        obj = Notificacion(cita_id, mensaje)
        
        # Ejecutar el método registrar
        resultadoAgregarJSONObject = json.loads(obj.registrar(cita_id))
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 
        else:
            return jsonify(resultadoAgregarJSONObject), 500 



@ws_notificacion.route('/notificacion/paciente/<int:paciente_id>', methods=['GET'])
#@vt.validar
def listar_notificacion_paciente(paciente_id):
    if request.method == 'GET':
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400 

        obj = Notificacion()

        resultadoPagoJSONObject = json.loads(obj.listar_notificacion_paciente(paciente_id))

        if resultadoPagoJSONObject['status']:
            return jsonify(resultadoPagoJSONObject), 200 # OK
        else:
            return jsonify(resultadoPagoJSONObject), 204 
        
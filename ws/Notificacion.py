import json
from flask import Blueprint, request, jsonify
from models.notificacion import Notificacion

ws_notificacion = Blueprint('ws_notificacion', __name__)

#
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

#
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
        
@ws_notificacion.route('/notificacion/paciente2/<int:paciente_id>', methods=['GET'])
#@vt.validar
def listar_notificacion_paciente2(paciente_id):
    if request.method == 'GET':
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400 

        obj = Notificacion()

        resultadoPagoJSONObject = json.loads(obj.listar_notificacion_paciente2(paciente_id))

        if resultadoPagoJSONObject['status']:
            return jsonify(resultadoPagoJSONObject), 200 # OK
        else:
            return jsonify(resultadoPagoJSONObject), 204 
        
#xdd
@ws_notificacion.route('/notificacion/paciente', methods=['PUT'])
def cambiar_estado_notificacion():
    if request.method == 'PUT':
        notificacion_id = request.form['notificacion_id']        
        leida = request.form['leida']

        leida_valor = 1
        if leida.upper() == 'LEÍDO':
            leida_valor = 0

        if not notificacion_id or not leida:
            return jsonify({'status': False, 'message': 'ID de notificación no válido'}), 400

        obj = Notificacion()

        resultado = json.loads(obj.actualizar_notificacion_paciente(notificacion_id, leida_valor))

        if resultado['status']:
            return jsonify(resultado), 200
        
        return jsonify(resultado), 500
    
#Anyelo
@ws_notificacion.route('/notificacion/actualizar_estado_aea', methods=['POST'])
def actualizar_estado_notificacion_aea():
    if request.method == 'POST':
        notificacion_id = request.form.get('notificacion_id')
        estado = request.form.get('estado')

        if not notificacion_id or estado is None:
            return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

        if estado not in ['0', '1']:
            return jsonify({'status': False, 'message': 'Estado inválido, debe ser 0 (no leída) o 1 (leída)'}), 400

        obj = Notificacion()
        resultadoActualizarJSONObject = json.loads(obj.actualizar_estado_aea(notificacion_id, int(estado)))

        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200
        else:
            return jsonify(resultadoActualizarJSONObject), 500
    

@ws_notificacion.route('/notificacion/actualizar_estado', methods=['POST'])
#@vt.validar
def actualizar_estado_notificacion():
    if request.method == 'POST':
        notificacion_id = request.form['notificacion_id']
        estado = request.form['estado']

        if not notificacion_id or estado is None:
            return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

        obj = Notificacion()
        resultadoActualizarJSONObject = json.loads(obj.actualizar_estado(notificacion_id, estado))

        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200
        else:
            return jsonify(resultadoActualizarJSONObject), 500

        
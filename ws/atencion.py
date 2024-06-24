from flask import Blueprint, request, jsonify
from models.atencion import Atencion
import json
import validarToken as vt

#Generar un modulo para gestionar el producto
ws_atencion = Blueprint('ws_atencion', __name__)

@ws_atencion.route('/atencion/lista/', defaults={'estado': None})
@ws_atencion.route('/atencion/lista/<estado>', methods=['GET'])
#@vt.validar
def lista(estado):
    if request.method == 'GET': 
        # Validar que el estado sea uno de los permitidos, si se ha proporcionado
        if estado and estado not in ['R', 'P', 'A', 'C']:
            return jsonify({'status': False, 'message': 'Estado no válido'}), 400  # Bad Request

        obj = Atencion()
        if estado:
            resultadoAtencionJSONObject = json.loads(obj.Lista_Atencion_PorEstado(estado))
        else:
            resultadoAtencionJSONObject = json.loads(obj.Lista_Atencion())

        if resultadoAtencionJSONObject['status'] == True:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        
@ws_atencion.route('/atencion/registrar', methods=['POST'])
#@vt.validar
def registrar_atencion():
    if request.method == 'POST':
        # Validar los parámetros de entrada necesarios para registrar una atención
        required_fields = ['paciente_id', 'odontologo_id', 'fecha', 'hora', 'motivo_consulta', 'diagnostico', 'costo', 'estado']
        if not all(field in request.form for field in required_fields):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

        # Leer los parámetros de entrada
        paciente_id = request.form['paciente_id']
        odontologo_id = request.form['odontologo_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo_consulta = request.form['motivo_consulta']
        diagnostico = request.form['diagnostico']
        anotacion = request.form.get('anotacion', '')
        costo = request.form['costo']
        estado = request.form['estado']

        # Instanciar el objeto de la clase Atencion
        obj = Atencion(0,paciente_id, odontologo_id, fecha, hora, motivo_consulta, diagnostico, anotacion, costo, estado)
        
        # Ejecutar el método registrar
        resultadoAgregarJSONObject = json.loads(obj.registrar())
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 # OK
        else:
            return jsonify(resultadoAgregarJSONObject), 500 # Internal Server Error
        
@ws_atencion.route('/atencion/actualizar', methods=['PUT'])
# @vt.validar
def actualizar_atencion():
    if request.method == 'PUT':
        # Validar los parámetros de entrada
        campos_requeridos = {'paciente_id', 'odontologo_id', 'fecha', 'hora', 'motivo_consulta', 'diagnostico', 'anotacion', 'costo', 'estado', 'id'}
        if campos_requeridos - set(request.form.keys()):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400
        
        # Leer los parámetros de entrada
        paciente_id = request.form['paciente_id']
        odontologo_id = request.form['odontologo_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo_consulta = request.form['motivo_consulta']
        diagnostico = request.form['diagnostico']
        anotacion = request.form['anotacion']
        costo = request.form['costo']
        estado = request.form['estado']
        id = request.form['id']
        
        if estado not in {'P', 'C', 'A', 'R'}:
            return jsonify({'status': False, 'data': None, 'message': 'Estado inválido. Solo se aceptan los valores P, C, A, R.'}), 400
        
        # Instanciar el objeto de la clase Atencion
        obj = Atencion(id, paciente_id, odontologo_id, fecha, hora, motivo_consulta, diagnostico, anotacion, costo, estado)
        
        # Ejecutar el método actualizar
        resultadoActualizarJSONObject = json.loads(obj.actualizar_atencion())
        
        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200 # OK
        else:
            return jsonify(resultadoActualizarJSONObject), 500 # Internal Server Error
        
    
@ws_atencion.route('/atencion/eliminar', methods=['DELETE'])
# @vt.validar
def eliminar_atencion():
    if request.method == 'DELETE':
        # Validar los parámetros de entrada
        if 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        
        # Leer el ID del registro a eliminar
        id = request.form['id']

        # Instanciar el objeto de la clase Atencion
        obj = Atencion(id, None, None, None, None, None, None, None, None, None)
        
        # Ejecutar el método eliminar
        resultadoEliminarJSONObject = json.loads(obj.eliminar_atencion())
        
        if resultadoEliminarJSONObject['status']:
            return jsonify(resultadoEliminarJSONObject), 200  # OK
        else:
            return jsonify(resultadoEliminarJSONObject), 500  # Internal Server Error


#APIS para paciente

@ws_atencion.route('/atencion/cita/registrar', methods=['POST'])
#@vt.validar
def registrar_cita():
    if request.method == 'POST':
        required_fields = ['paciente_id', 'odontologo_id', 'fecha', 'hora', 'motivo_consulta']
        if not all(field in request.form for field in required_fields):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

        paciente_id = request.form['paciente_id']
        odontologo_id = request.form['odontologo_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo_consulta = request.form['motivo_consulta']
        diagnostico = None
        anotacion = None
        costo = None
        estado = None

        obj = Atencion(0,paciente_id, odontologo_id, fecha, hora, motivo_consulta, diagnostico, anotacion, costo, estado)
        
        resultadoAgregarJSONObject = json.loads(obj.registrar_cita_atencion_por_paciente())
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 # OK
        else:
            return jsonify(resultadoAgregarJSONObject), 500 # Internal Server Error
        

@ws_atencion.route('/atencion/citas-paciente/<int:paciente_id>', methods=['GET'])
#@vt.validar
def obtener_citas_paciente(paciente_id):
    if request.method == 'GET': 
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400  # Bad Request

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_citas_por_paciente(paciente_id))


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content


@ws_atencion.route('/atencion/cita/cancelar', methods=['POST'])
#@vt.validar
def cancelar_cita():
    if request.method == 'POST':
        required_fields = ['cita_id']
        if not all(field in request.form for field in required_fields):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

        cita_id = request.form['cita_id']
        paciente_id = None
        odontologo_id = None
        fecha = None
        hora = None
        motivo_consulta = None
        diagnostico = None
        anotacion = None
        costo = None
        estado = None

        obj = Atencion(cita_id, paciente_id, odontologo_id, fecha, hora, motivo_consulta, diagnostico, anotacion, costo, estado)
        

        resultadoAgregarJSONObject = json.loads(obj.cancelar_cita_atencion_por_paciente())
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 # OK
        else:
            return jsonify(resultadoAgregarJSONObject), 500 # Internal Server Error
        
@ws_atencion.route('/atencion/cita/reprogramar', methods=['POST'])
#@vt.validar
def reprogramar_cita():
    if request.method == 'POST':
        required_fields = ['cita_id', 'fecha', 'hora']
        if not all(field in request.form for field in required_fields):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400

        cita_id = request.form['cita_id']
        paciente_id = None
        odontologo_id = None
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo_consulta = None
        diagnostico = None
        anotacion = None
        costo = None
        estado = None

        obj = Atencion(cita_id, paciente_id, odontologo_id, fecha, hora, motivo_consulta, diagnostico, anotacion, costo, estado)
        

        resultadoAgregarJSONObject = json.loads(obj.reprogramar_cita_atencion_por_paciente())
        
        if resultadoAgregarJSONObject['status'] == True:
            return jsonify(resultadoAgregarJSONObject), 200 # OK
        else:
            return jsonify(resultadoAgregarJSONObject), 500 # Internal Server Error
        


@ws_atencion.route('/atencion/historial/<int:paciente_id>', methods=['GET'])
#@vt.validar
def obtener_historial_paciente(paciente_id):
    if request.method == 'GET': 
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400  # Bad Request

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_historial_por_paciente(paciente_id))


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        
@ws_atencion.route('/atencion/detalle-historial/<int:cita_id>', methods=['GET'])
#@vt.validar
def obtener_detalle_historial_paciente(cita_id):
    if request.method == 'GET': 
        if not cita_id:
            return jsonify({'status': False, 'message': 'ID de cita no válido'}), 400  # Bad Request

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_detalle_historial_por_paciente(cita_id))


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
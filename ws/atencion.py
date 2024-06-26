from flask import Blueprint, request, jsonify
from models.atencion import Atencion
import json
import validarToken as vt
from bd import Conexion as db

#Generar un modulo para gestionar el atencion al paciente
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


@ws_atencion.route('/atencion/cita/cancelar', methods=['PUT'])
#@vt.validar
def cancelar_cita():
    if request.method == 'PUT':
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
        
        
@ws_atencion.route('/atencion/cita/reprogramar', methods=['PUT'])
#@vt.validar
def reprogramar_cita():
    if request.method == 'PUT':
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
              
    
@ws_atencion.route('/atencion/citas/', methods=['GET'])
#@vt.validar
def obtener_citas():
    if request.method == 'GET': 

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_citas())


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        
        
@ws_atencion.route('/atencion/citas/pacientes', methods=['GET'])
@vt.validar
def obtenerPacientes():
    if request.method == 'GET': 

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtenerPacientes())


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        
        
@ws_atencion.route('/atencion/citas/odontologos', methods=['GET'])
@vt.validar
def obtenerOdontologos():
    if request.method == 'GET': 

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtenerOdontologos())


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content


@ws_atencion.route('/atencion/odontologos', methods=['GET'])
#@vt.validar
def obtener_odontologos():
    if request.method == 'GET': 

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_odontologos())


        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        
        
@ws_atencion.route('/atencion/citas-por-odontologo/<int:odontologo_id>', methods=['GET'])
def obtener_citas_por_odontologo(odontologo_id):
    if request.method == 'GET': 
        if not odontologo_id:
            return jsonify({'status': False, 'message': 'ID de odontólogo no válido'}), 400  # Bad Request

        obj = Atencion()
        resultadoAtencionJSONObject = json.loads(obj.obtener_citas_por_odontologo(odontologo_id))

        if resultadoAtencionJSONObject['status']:
            return jsonify(resultadoAtencionJSONObject), 200 # OK
        else:
            return jsonify(resultadoAtencionJSONObject), 204 # No Content
        

@ws_atencion.route('/atencion/detalle-cita/<int:cita_id>', methods=['GET'])
def obtener_detalle_cita(cita_id):
    if request.method == 'GET':
        if not cita_id:
            return jsonify({'status': False, 'message': 'ID de cita no válido'}), 400  # Bad Request

        obj = Atencion()
        resultadoCitaJSONObject = json.loads(obj.obtener_cita_por_id(cita_id))

        if resultadoCitaJSONObject['status']:
            return jsonify(resultadoCitaJSONObject), 200  # OK
        else:
            return jsonify(resultadoCitaJSONObject), 404  # Not Found
        
        
@ws_atencion.route('/cita/actualizar', methods=['PUT'])
def actualizar_atencion2():
    if request.method == 'PUT':
        # Validar los parámetros de entrada
        if 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta el parametro id'}), 400
        
        # Leer los parámetros de entrada
        diagnostico = request.form.get('diagnostico', None)
        anotacion = request.form.get('anotacion', None)
        cita_id = request.form['id']
        
        # Instanciar el objeto de la clase Atencion
        obj = Atencion(cita_id=cita_id, diagnostico=diagnostico, anotacion=anotacion)
        
        # Ejecutar el método actualizar
        resultadoActualizarJSONObject = json.loads(obj.actualizar_cita())
        
        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200 # OK
        else:
            return jsonify(resultadoActualizarJSONObject), 500 # Internal Server Error
        
@ws_atencion.route('/cita/registrar_completa', methods=['POST'])
def registrar_completa():
    if request.method == 'POST':
        # Validar los parámetros de entrada
        if 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta el parametro id'}), 400
        
        cita_id = request.form['id']
        diagnostico = request.form.get('diagnostico', None)
        anotacion = request.form.get('anotacion', None)
        tratamientos = request.form.getlist('tratamientos')
        recetas = request.form.getlist('recetas')

        # Convertir las recetas de JSON string a diccionario
        try:
            recetas = [json.loads(receta) for receta in recetas]
        except json.JSONDecodeError as e:
            return jsonify({'status': False, 'message': 'Error en el formato de recetas: ' + str(e)}), 400

        con = db().open
        cursor = con.cursor()

        try:
            # Iniciar transacción
            con.begin()

            # Actualizar diagnóstico y anotaciones
            sql_atencion = """
            UPDATE cita_atencion
            SET diagnostico = COALESCE(%s, diagnostico),
                anotacion = COALESCE(%s, anotacion)
            WHERE id = %s
            """
            cursor.execute(sql_atencion, (diagnostico, anotacion, cita_id))

            # Registrar tratamientos
            for tratamiento_id in tratamientos:
                sql_tratamiento = """
                INSERT INTO atencion_tratamiento (atencion_id, tratamiento_id, estado)
                VALUES (%s, %s, '5')
                """
                cursor.execute(sql_tratamiento, (cita_id, tratamiento_id))

            # Registrar recetas
            for receta in recetas:
                medicamento = receta['medicamento']
                dosis = receta['dosis']
                sql_receta = """
                INSERT INTO receta (atencion_id, medicamento, dosis)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql_receta, (cita_id, medicamento, dosis))

            # Confirmar transacción
            con.commit()
            cursor.close()
            con.close()
            return jsonify({'status': True, 'message': 'Registro completo exitosamente'})

        except Exception as e:
            # Revertir transacción en caso de error
            con.rollback()
            cursor.close()
            con.close()
            return jsonify({'status': False, 'message': str(e)}), 500






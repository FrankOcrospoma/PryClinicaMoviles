from flask import Blueprint, request, jsonify
from models.atencion_tratamiento import AtencionTratamiento
import json
import validarToken as vt

ws_atencion_tratamiento = Blueprint('ws_atencion_tratamiento', __name__)

@ws_atencion_tratamiento.route('/atencion_tratamiento/registrar', methods=['POST'])
def registrar_atencion_tratamiento():
    if request.method == 'POST':
        if 'cita_id' not in request.form or 'tratamiento_id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400
        
        cita_id = request.form['cita_id']
        tratamiento_id = request.form['tratamiento_id']
        
        # Instanciar el objeto de la clase AtencionTratamiento
        obj = AtencionTratamiento(cita_id=cita_id, tratamiento_id=tratamiento_id)
        
        # Ejecutar el método registrar
        resultadoRegistrarJSONObject = json.loads(obj.registrar_atencion_tratamiento())
        
        if resultadoRegistrarJSONObject['status']:
            return jsonify(resultadoRegistrarJSONObject), 200 # OK
        else:
            return jsonify(resultadoRegistrarJSONObject), 500 # Internal Server Error

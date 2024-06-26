from flask import Blueprint, request, jsonify
from models.receta import Receta
import json
import validarToken as vt

ws_receta = Blueprint('ws_receta', __name__)

@ws_receta.route('/receta/registrar', methods=['POST'])
def registrar_receta():
    if request.method == 'POST':
        if 'cita_id' not in request.form or 'medicamento' not in request.form or 'dosis' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parametros'}), 400

        cita_id = request.form['cita_id']
        medicamento = request.form['medicamento']
        dosis = request.form['dosis']

        # Instanciar el objeto de la clase Receta
        obj = Receta(cita_id=cita_id, medicamento=medicamento, dosis=dosis)

        # Ejecutar el método registrar
        resultadoRegistrarJSONObject = json.loads(obj.registrar_receta())

        if resultadoRegistrarJSONObject['status']:
            return jsonify(resultadoRegistrarJSONObject), 200  # OK
        else:
            return jsonify(resultadoRegistrarJSONObject), 500  # Internal Server Error
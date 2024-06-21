from flask import Blueprint, request, jsonify
from models.usuario import Usuario
import json
import validarToken as vt

ws_usuario = Blueprint('ws_usuario', __name__)

@ws_usuario.route('/usuario/agregar', methods=['POST'])
# @vt.validar
def agregar_usuario():
    if request.method == 'POST':
        required_params = ['nombreUsuario', 'email', 'contrasena', 'estado', 'token', 'estadoToken', 'nombre', 'apeCompleto', 'fechaNac', 'documento', 'tipo_documento_id', 'sexo', 'direccion', 'telefono', 'foto', 'rolId']
        if not all(param in request.form for param in required_params):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        nombre_usuario = request.form['nombreUsuario']
        email = request.form['email']
        contrasena = request.form['contrasena']
        estado = request.form['estado']
        token = request.form['token']
        estado_token = request.form['estadoToken']
        nombre = request.form['nombre']
        ape_completo = request.form['apeCompleto']
        fecha_nac = request.form['fechaNac']
        documento = request.form['documento']
        tipo_documento_id = request.form['tipo_documento_id']
        sexo = request.form['sexo']
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')
        foto = request.form.get('foto', '')
        rol_id = request.form['rolId']
        obj = Usuario(None, nombre_usuario, email, contrasena, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id)
        resultado_agregar = json.loads(obj.agregar())
        if resultado_agregar['status']:
            return jsonify(resultado_agregar), 200
        else:
            return jsonify(resultado_agregar), 500

@ws_usuario.route('/usuario/actualizar', methods=['PUT'])
@vt.validar
def actualizar_usuario():
    if request.method == 'PUT':
        required_params = ['id', 'nombreUsuario', 'email', 'estado', 'token', 'estadoToken', 'nombre', 'apeCompleto', 'fechaNac', 'documento', 'tipo_documento_id','sexo', 'direccion', 'telefono', 'foto', 'rolId']
        if not all(param in request.form for param in required_params):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        id_usuario = request.form['id']
        nombre_usuario = request.form['nombreUsuario']
        email = request.form['email']

        estado = request.form['estado']
        token = request.form['token']
        estado_token = request.form['estadoToken']
        nombre = request.form['nombre']
        ape_completo = request.form['apeCompleto']
        fecha_nac = request.form['fechaNac']
        documento = request.form['documento']
        tipo_documento_id = request.form['tipo_documento_id']
        sexo = request.form['sexo']
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')
        foto = request.form.get('foto', '')
        rol_id = request.form['rolId']
        obj = Usuario(id_usuario, nombre_usuario, email, None, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id)
        resultado_actualizar = json.loads(obj.actualizar())
        if resultado_actualizar['status']:
            return jsonify(resultado_actualizar), 200
        else:
            return jsonify(resultado_actualizar), 500

@ws_usuario.route('/usuario/eliminar', methods=['DELETE'])
@vt.validar
def eliminar_usuario():
    if request.method == 'DELETE':
        if 'id' not in request.form:
            return jsonify({'status': False, 'data': None, 'message': 'Falta el parámetro id'}), 400
        id_usuario = request.form['id']
        obj = Usuario(id_usuario)
        resultado_eliminar = json.loads(obj.eliminar())
        if resultado_eliminar['status']:
            return jsonify(resultado_eliminar), 200
        else:
            return jsonify(resultado_eliminar), 500

@ws_usuario.route('/usuario/lista', methods=['GET'])
@vt.validar
def listar_usuarios():
    if request.method == 'GET':
        obj = Usuario()
        return jsonify(json.loads(obj.listar_usuarios())), 200

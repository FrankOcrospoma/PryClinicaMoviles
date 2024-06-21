from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models.usuario import Usuario
import os
import json
import validarToken as vt

ws_usuario = Blueprint('ws_usuario', __name__)

# Define una ruta absoluta para UPLOAD_FOLDER
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'img')  # Asegúrate de que esta ruta existe en tu sistema de archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@ws_usuario.route('/usuario/subirFoto', methods=['POST'])
@vt.validar
def subir_foto():
    if 'foto' not in request.files:
        return jsonify({'status': False, 'data': None, 'message': 'No se encontró el archivo'}), 400
    file = request.files['foto']
    if file.filename == '':
        return jsonify({'status': False, 'data': None, 'message': 'No se seleccionó ningún archivo'}), 400
    if file and allowed_file(file.filename):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'status': True, 'data': {'filename': filename, 'filepath': file_path}, 'message': 'Archivo subido exitosamente'}), 200
    return jsonify({'status': False, 'data': None, 'message': 'Tipo de archivo no permitido'}), 400

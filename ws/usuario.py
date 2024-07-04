from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.usuario import Usuario
import os
import json
import hashlib
import validarToken as vt
from github import Github
import random
import smtplib
from email.mime.text import MIMEText

ws_usuario = Blueprint('ws_usuario', __name__)

# Define una ruta absoluta para UPLOAD_FOLDER
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = 'FrankOcrospoma/PryClinicaMoviles'
BRANCH_NAME = 'main'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_github(filename, filepath):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    with open(filepath, 'rb') as file:
        content = file.read()
    repo.create_file(f'img/{filename}', f'Subir archivo {filename}', content, branch=BRANCH_NAME)

@ws_usuario.route('/usuario/agregar', methods=['POST'])
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
        required_params = ['id', 'nombreUsuario', 'email', 'estado', 'token', 'estadoToken', 'nombre', 'apeCompleto', 'fechaNac', 'documento', 'tipo_documento_id', 'sexo', 'direccion', 'telefono', 'foto', 'rolId']
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

#Anyelo
@ws_usuario.route('/usuario/actualizar_estado_aea', methods=['POST'])
def actualizar_estado_notificacion_aea():
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        notificacion = request.form.get('notificacion')

        if not usuario_id or notificacion is None:
            return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

        if notificacion not in ['0', '1']:
            return jsonify({'status': False, 'message': 'Estado inválido, debe ser 0 (no leída) o 1 (leída)'}), 400

        obj = Usuario()
        resultadoActualizarJSONObject = json.loads(obj.actualizar_estado_aea(usuario_id, int(notificacion)))

        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200
        else:
            return jsonify(resultadoActualizarJSONObject), 500


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
    
    
@ws_usuario.route('/usuario/lista/pacientes', methods=['GET'])
@vt.validar
def listar_usuarios_pacientes():
    if request.method == 'GET':
        obj = Usuario()
        return jsonify(json.loads(obj.listar_usuarios_pacientes())), 200
    
@ws_usuario.route('/usuario/lista/odontologos', methods=['GET'])
@vt.validar
def listar_usuarios_odontologos():
    if request.method == 'GET':
        obj = Usuario()
        return jsonify(json.loads(obj.listar_usuarios_odontologos())), 200

@ws_usuario.route('/usuario/subirFoto', methods=['POST'])
@vt.validar
def subir_foto():
    print("Inicio de subir_foto")
    if 'foto' not in request.files:
        print("No se encontró el archivo 'foto' en la solicitud")
        return jsonify({'status': False, 'data': None, 'message': 'No se encontró el archivo'}), 400
    file = request.files['foto']
    if file.filename == '':
        print("No se seleccionó ningún archivo")
        return jsonify({'status': False, 'data': None, 'message': 'No se seleccionó ningún archivo'}), 400
    if file and allowed_file(file.filename):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            print(f"Carpeta {UPLOAD_FOLDER} creada")
        else:
            print(f"Carpeta {UPLOAD_FOLDER} ya existe")
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Verificar si el archivo ya existe
        if os.path.exists(filepath):
            print(f"Archivo {filename} ya existe, utilizando el existente")
            return jsonify({'status': True, 'data': {'filename': filename}, 'message': 'Archivo ya existente utilizado'}), 200
        
        # Guardar el archivo si no existe
        file.save(filepath)
        print(f"Archivo guardado en {filepath}")
        
        # Verificar si el archivo se guardó correctamente
        if os.path.exists(filepath):
            print(f"Archivo {filename} subido exitosamente")
            try:
                upload_to_github(filename, filepath)
                print(f"Archivo {filename} subido a GitHub exitosamente")
                return jsonify({'status': True, 'data': {'filename': filename}, 'message': 'Archivo subido exitosamente'}), 200
            except Exception as e:
                print(f"Error al subir el archivo a GitHub: {str(e)}")
                return jsonify({'status': False, 'data': None, 'message': 'Error al subir el archivo a GitHub'}), 500
        else:
            print(f"No se pudo guardar el archivo {filename}")
            return jsonify({'status': False, 'data': None, 'message': 'No se pudo guardar el archivo'}), 500
    print("Tipo de archivo no permitido")
    return jsonify({'status': False, 'data': None, 'message': 'Tipo de archivo no permitido'}), 400

@ws_usuario.route('/img/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@ws_usuario.route('/usuario/cambiarContrasena', methods=['POST'])
@vt.validar
def cambiar_contrasena():
    if request.method == 'POST':
        required_params = ['id', 'nuevaContrasena']
        if not all(param in request.form for param in required_params):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        
        id_usuario = request.form['id']
        nueva_contrasena = request.form['nuevaContrasena']
        
        obj = Usuario(id_usuario)
        resultado_cambiar = json.loads(obj.cambiar_contrasena(nueva_contrasena))
        if resultado_cambiar['status']:
            return jsonify(resultado_cambiar), 200
        else:
            return jsonify(resultado_cambiar), 500
        
@ws_usuario.route('/usuario/enviarCodigoRecuperacion', methods=['POST'])
def enviar_codigo_recuperacion():
    email = request.form.get('email')
    if not email:
        return jsonify({'status': False, 'message': 'Falta el correo electrónico'}), 400

    usuario = Usuario.buscar_por_email(email)
    if not usuario:
        return jsonify({'status': False, 'message': 'Correo electrónico no encontrado'}), 404

    codigo = ''.join(random.choices('0123456789', k=6))

    # Aquí debes guardar el código en la base de datos asociado al usuario
    try:
        usuario.guardar_codigo_recuperacion(codigo)
    except Exception as e:
        print(f"Error al guardar el código de recuperación en la base de datos: {e}")
        return jsonify({'status': False, 'message': 'Error al guardar el código de recuperación en la base de datos'}), 500

    try:
        print(f"Creando mensaje de correo para {email} con código {codigo}")
        msg = MIMEMultipart()
        msg['Subject'] = 'Recuperación de contraseña'
        msg['From'] = 'ocrospomaugazfrank@gmail.com'
        msg['To'] = email

        body = MIMEText(f'Tu código de verificación es: {codigo}', 'plain', 'utf-8')
        msg.attach(body)

        print(f"Mensaje creado: {msg}")

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("Conexión al servidor SMTP establecida")
            # Aquí utiliza la contraseña específica de la aplicación generada
            server.login('ocrospomaugazfrank@gmail.com', 'qwdw lumx nube dkhh')
            print("Inicio de sesión en el servidor SMTP exitoso")
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f"Correo enviado a {email}")

        return jsonify({'status': True, 'message': 'Código enviado'}), 200
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")
        return jsonify({'status': False, 'message': str(e)}), 500


@ws_usuario.route('/usuario/verificarCodigo', methods=['POST'])
def verificar_codigo():
    email = request.form.get('email')
    codigo = request.form.get('codigo')

    if not email or not codigo:
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    usuario = Usuario.buscar_por_email(email)
    if not usuario or not usuario.verificar_codigo(codigo):
        return jsonify({'status': False, 'message': 'Código incorrecto'}), 400

    return jsonify({'status': True, 'message': 'Código verificado'}), 200

@ws_usuario.route('/usuario/restablecerContrasena', methods=['POST'])
def restablecer_contrasena():
    email = request.form.get('email')
    nueva_contrasena = request.form.get('nuevaContrasena')

    if not email or not nueva_contrasena:
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    usuario = Usuario.buscar_por_email(email)
    if not usuario:
        return jsonify({'status': False, 'message': 'Usuario no encontrado'}), 404

    usuario.cambiar_contrasena(nueva_contrasena)

    return jsonify({'status': True, 'message': 'Contraseña restablecida'}), 200

#paciente

@ws_usuario.route('/usuario/agregar/paciente', methods=['POST'])
def agregar_paciente():
    if request.method == 'POST':
        required_params = ['nombreUsuario', 'email', 'contrasena', 'estado', 'nombre', 'apeCompleto', 'fechaNac', 'documento', 'tipo_documento_id', 'sexo', 'direccion', 'telefono']
        if not all(param in request.form for param in required_params):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        nombre_usuario = request.form['nombreUsuario']
        email = request.form['email']
        contrasena = request.form['contrasena']
        estado = 1
        token = None
        estado_token = 1
        nombre = request.form['nombre']
        ape_completo = request.form['apeCompleto']
        fecha_nac = request.form['fechaNac']
        documento = request.form['documento']
        tipo_documento_id = request.form['tipo_documento_id']
        sexo = request.form['sexo']
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')

        # Cifrar la contraseña en MD5
        md5_hash = hashlib.md5()
        md5_hash.update(contrasena.encode('utf-8'))
        contrasena_md5 = md5_hash.hexdigest()

        foto = None
        rol_id = None
        obj = Usuario(None, nombre_usuario, email, contrasena_md5, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id)
        resultado_agregar = json.loads(obj.agregar_paciente())
        if resultado_agregar['status']:
            return jsonify(resultado_agregar), 200
        else:
            return jsonify(resultado_agregar), 500
        
        
@ws_usuario.route('/usuario/agregar/odontologo', methods=['POST'])
def agregar_odontologo():
    if request.method == 'POST':
        required_params = ['nombreUsuario', 'email', 'contrasena', 'estado', 'nombre', 'apeCompleto', 'fechaNac', 'documento', 'tipo_documento_id', 'sexo', 'direccion', 'telefono']
        if not all(param in request.form for param in required_params):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        nombre_usuario = request.form['nombreUsuario']
        email = request.form['email']
        contrasena = request.form['contrasena']
        estado = 1
        token = None
        estado_token = 1
        nombre = request.form['nombre']
        ape_completo = request.form['apeCompleto']
        fecha_nac = request.form['fechaNac']
        documento = request.form['documento']
        tipo_documento_id = request.form['tipo_documento_id']
        sexo = request.form['sexo']
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')

        # Cifrar la contraseña en MD5
        md5_hash = hashlib.md5()
        md5_hash.update(contrasena.encode('utf-8'))
        contrasena_md5 = md5_hash.hexdigest()

        foto = None
        rol_id = None
        obj = Usuario(None, nombre_usuario, email, contrasena_md5, estado, token, estado_token, nombre, ape_completo, fecha_nac, documento, tipo_documento_id, sexo, direccion, telefono, foto, rol_id)
        resultado_agregar = json.loads(obj.agregar_odontologo())
        if resultado_agregar['status']:
            return jsonify(resultado_agregar), 200
        else:
            return jsonify(resultado_agregar), 500
        

@ws_usuario.route('/usuario/paciente/historial/<int:paciente_id>', methods=['GET'])
#@vt.validar
def historial_usuario_paciente(paciente_id):
    if request.method == 'GET':
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400  # Bad Request

        obj = Usuario()
        return jsonify(json.loads(obj.listar_usuarios_pacientes())), 200
    
@ws_usuario.route('/usuario/notificar/paciente', methods=['POST'])
def notificar():
    if request.method == 'POST':
        data = {}
        data["paciente_id"] = request.form.get('paciente_id')
        data["mensaje"] = request.form.get('mensaje')
        data["leida"] = 0

        obj = Usuario()

        resultado = json.loads(obj.notificar_paciente(data))

        if resultado["status"]:
            return jsonify(resultado), 200

        return jsonify(resultado), 400
    

@ws_usuario.route('/usuario/paciente/notificaciones/<int:paciente_id>', methods=['GET'])
#@vt.validar
def notificaciones_paciente(paciente_id):
    if request.method == 'GET':
        if not paciente_id:
            return jsonify({'status': False, 'message': 'ID de paciente no válido'}), 400  # Bad Request

        obj = Usuario()
        return jsonify(json.loads(obj.lista_notificaciones_paciente(paciente_id))), 200
    
    
@ws_usuario.route('/usuario/actualizar/notificacion/frank', methods=['POST'])
#@vt.validar
def actualizar_estado_notificacion():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        notificacion = request.form['notificacion']

        if not usuario_id or notificacion is None:
            return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

        obj = Usuario()
        resultadoActualizarJSONObject = json.loads(obj.actualizar_estado_notificacion(usuario_id, notificacion))

        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200
        else:
            return jsonify(resultadoActualizarJSONObject), 500
    
@ws_usuario.route('/usuario/actualizar_estado_geancarlos', methods=['POST'])
#@vt.validar
def actualizar_estado_notificacion_geancarlos():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        estado = request.form['estado']

        if not usuario_id or estado is None:
            return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

        obj = Usuario()
        resultadoActualizarJSONObject = json.loads(obj.actualizar_estado_notificacion_geancarlos(usuario_id, estado))

        if resultadoActualizarJSONObject['status']:
            return jsonify(resultadoActualizarJSONObject), 200
        else:
            return jsonify(resultadoActualizarJSONObject), 500
        


#edu
@ws_usuario.route('/notificacion/paciente/estado', methods=['PUT'])
def cambiar_estado_notificacion_por_paciente():
    if request.method == 'PUT':
        paciente_id = request.form['paciente_id']        
        notificacion = request.form['notificacion']


        obj = Usuario()

        resultado = json.loads(obj.cambiar_estado_notificacion_por_paciente(paciente_id, notificacion))

        if resultado['status']:
            return jsonify(resultado), 200
        
        return jsonify(resultado), 500
    
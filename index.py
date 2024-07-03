from flask import Flask, render_template
# Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.atencion import ws_atencion
from ws.usuario import ws_usuario
from ws.especialidad import ws_especialidad
from ws.pago import ws_pago
from ws.tratamiento import ws_tratamiento
from ws.rol import ws_rol
from ws.seguro_dental import ws_seguro_dental
from ws.atencion_tratamiento import ws_atencion_tratamiento
from ws.receta import ws_receta
from ws.Notificacion import ws_notificacion
from routes.informeCitas import main as informeCitas_bp  # Importar el blueprint de informeCitas
from routes.tratamientoPaciente import main as tratamientoPaciente_bp

# Crear la variable de aplicación con Flask
app = Flask(__name__)

# Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)   
app.register_blueprint(ws_atencion)
app.register_blueprint(ws_usuario)
app.register_blueprint(ws_especialidad)
app.register_blueprint(ws_tratamiento)
app.register_blueprint(ws_pago)
app.register_blueprint(ws_rol)
app.register_blueprint(ws_seguro_dental)
app.register_blueprint(ws_atencion_tratamiento)
app.register_blueprint(ws_receta)
app.register_blueprint(informeCitas_bp)  # Registrar el blueprint de informeCitas
app.register_blueprint(tratamientoPaciente_bp)
app.register_blueprint(ws_notificacion)

@app.route('/')
def home():
    return render_template('index.html')

# Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(debug=True)

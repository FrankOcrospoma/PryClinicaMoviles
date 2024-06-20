from flask import Flask
#Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.producto import ws_producto
from ws.atencion import ws_atencion
from ws.usuario import ws_usuario
from ws.especialidad import ws_especialidad
from ws.pago import ws_pago
from ws.tratamiento import ws_tratamiento
from ws.rol import ws_rol
from ws.seguro_dental import ws_seguro_dental
#from ws.sesion import ws_sesion

#Crear la variable de aplicación con Flask
app = Flask(__name__)


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)   
app.register_blueprint(ws_producto)
app.register_blueprint(ws_atencion)
app.register_blueprint(ws_usuario)
app.register_blueprint(ws_especialidad)
app.register_blueprint(ws_tratamiento)
app.register_blueprint(ws_pago)
app.register_blueprint(ws_rol)
app.register_blueprint(ws_seguro_dental)

@app.route('/')
def home():
    return 'Servicios web en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(debug=True)

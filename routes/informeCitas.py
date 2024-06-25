from flask import Flask, Blueprint, redirect, request, jsonify, render_template
from conexion import obtener_conexion
from datetime import datetime

main = Blueprint("informeCitas", __name__, url_prefix="/informeCitas")

def obtener_informes_citas(fecha_inicio, fecha_fin, paciente_id=None, odontologo_id=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
        SELECT 
            cita_atencion.*,
            paciente.nombre AS paciente_nombre,
            paciente.ape_completo AS paciente_apellidos,
            paciente.documento AS paciente_dni,
            odontologo.nombre AS odontologo_nombre,
            odontologo.ape_completo AS odontologo_apellidos,
            odontologo.documento AS odontologo_dni
        FROM cita_atencion
        JOIN usuario AS paciente ON cita_atencion.paciente_id = paciente.id
        JOIN usuario AS odontologo ON cita_atencion.odontologo_id = odontologo.id
        WHERE fecha BETWEEN %s AND %s
    """
    parametros = [fecha_inicio, fecha_fin]

    if paciente_id:
        query += " AND paciente_id = %s"
        parametros.append(paciente_id)
    
    if odontologo_id:
        query += " AND odontologo_id = %s"
        parametros.append(odontologo_id)
    
    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

def obtener_pacientes_y_odontologos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    query_pacientes = "SELECT id, nombre, ape_completo FROM usuario WHERE rol_id = 2"  # Rol de paciente
    cursor.execute(query_pacientes)
    pacientes = cursor.fetchall()

    query_odontologos = "SELECT id, nombre, ape_completo FROM usuario WHERE rol_id = 3"  # Rol de odontólogo
    cursor.execute(query_odontologos)
    odontologos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return pacientes, odontologos


@main.route('/consultar', methods=['GET', 'POST'])
def consultar_informes():
    pacientes, odontologos = obtener_pacientes_y_odontologos()

    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        paciente_id = request.form.get('paciente_id')
        odontologo_id = request.form.get('odontologo_id')

        informes = obtener_informes_citas(fecha_inicio, fecha_fin, paciente_id, odontologo_id)
        return render_template('informeCitas.html', informes=informes, pacientes=pacientes, odontologos=odontologos)

    return render_template('informeCitas.html', pacientes=pacientes, odontologos=odontologos)


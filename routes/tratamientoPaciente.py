from flask import Blueprint, request, render_template
from conexion import obtener_conexion
from datetime import datetime

main = Blueprint("tratamientoPaciente", __name__, url_prefix="/tratamientoPaciente")

def obtener_informe_pacientes_tratamientos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
        SELECT
            usuario.id AS paciente_id,
            CONCAT(usuario.nombre, ' ', usuario.ape_completo) AS nombre_paciente,
            tratamiento.id AS tratamiento_id,
            tratamiento.nombre AS nombre_tratamiento,
            tratamiento.descripcion AS descripcion_tratamiento,
            tratamiento.costo AS costo_tratamiento
        FROM
            usuario
        JOIN
            cita_atencion ON usuario.id = cita_atencion.paciente_id
        JOIN
            atencion_tratamiento ON cita_atencion.id = atencion_tratamiento.atencion_id
        JOIN
            tratamiento ON atencion_tratamiento.tratamiento_id = tratamiento.id
        WHERE
            usuario.rol_id = 2
        ORDER BY
            usuario.id, tratamiento.id;
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados

@main.route('/informe', methods=['GET'])
def informe_pacientes_tratamientos():
    informe = obtener_informe_pacientes_tratamientos()
    return render_template('tratamientoPaciente.html', informe=informe)

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from app.state import ultima_consulta
from app.database import conectar_db, obtener_historial_placas
from app.config import URL, USERNAME, PASSWORD
from app.camera import get_plates, verificar_conexion_camara

# Crear un Blueprint para las rutas
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ruta principal que renderiza la plantilla index.html."""
    return render_template('index.html')

@main_bp.route('/datos')
def datos():
    """Endpoint JSON que devuelve los datos actuales de la última consulta."""
    # Verificar el estado actual de la conexión con la cámara
    conectado, mensaje = verificar_conexion_camara()
    estado_conexion = {
        "camara_conectada": conectado,
        "mensaje_estado": mensaje
    }
    
    # Combinar la información de la última consulta con el estado de conexión
    datos_respuesta = {**ultima_consulta, **estado_conexion}
    
    return jsonify(datos_respuesta)

@main_bp.route('/admin')
def admin():
    """Ruta para la página de administración."""
    # Obtener parámetros de paginación de la URL
    pagina = request.args.get('pagina', 1, type=int)
    registros_por_pagina = request.args.get('por_pagina', 10, type=int)
    filtro_placa = request.args.get('placa', None)
    
    # Verificar la conexión con la cámara
    conectado, mensaje_conexion = verificar_conexion_camara()
    placas = get_plates()
    
    # Obtener información de la cámara actual
    camara_info = {
        "url": URL,
        "usuario": USERNAME,
        "modelo": "IDS-2CD7A46G0/P-IZHSY",
        "estado": "Activo" if conectado else "Sin conexión",
        "eventos_recientes": len(placas) if placas else 0,
        "mensaje": mensaje_conexion
    }
    
    # Obtener historial de detecciones desde el servidor remoto con paginación
    resultado_historial = obtener_historial_placas(
        pagina=pagina, 
        registros_por_pagina=registros_por_pagina,
        filtro_placa=filtro_placa
    )
    
    # Extraer la información de paginación
    registros = resultado_historial.get("registros", [])
    
    # Pasar toda la información de paginación a la plantilla
    info_paginacion = {
        "pagina_actual": resultado_historial.get("pagina_actual", 1),
        "total_paginas": resultado_historial.get("total_paginas", 1),
        "total_registros": resultado_historial.get("total_registros", 0),
        "registros_por_pagina": registros_por_pagina,
        "filtro_placa": filtro_placa
    }
    
    return render_template('admin.html', 
                           camara=camara_info, 
                           historial=registros,
                           paginacion=info_paginacion)

@main_bp.route('/verificar-conexion')
def verificar_conexion():
    """Endpoint para verificar la conexión con la cámara."""
    conectado, mensaje = verificar_conexion_camara()
    placas = get_plates()
    estado = {
        "estado": "Activo" if conectado else "Sin conexión",
        "eventos_recientes": len(placas) if placas else 0,
        "mensaje": mensaje
    }
    return jsonify(estado) 
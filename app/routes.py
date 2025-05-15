"""
Módulo de rutas y controladores web para el Sistema de Detección de Placas

Este módulo define todas las rutas HTTP que expone la aplicación web Flask.
Implementa los controladores que procesan las solicitudes web entrantes y
generan las respuestas correspondientes. Las principales funcionalidades son:

1. Página principal (index) que muestra la última placa detectada y su estado de cita
2. Endpoint JSON para obtener los datos actualizados de la última detección
3. Panel de administración para monitorear el sistema y ver el historial
4. Endpoint para verificar el estado de conexión con la cámara

El módulo utiliza el patrón Blueprint de Flask para organizar las rutas
de manera modular y facilitar su mantenimiento.
"""

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from app.state import ultima_consulta
from app.database import conectar_db, obtener_historial_placas
from app.config import URL, USERNAME, PASSWORD
from app.camera import get_plates, verificar_conexion_camara

# Crear un Blueprint para las rutas
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Ruta principal que muestra la interfaz de usuario del sistema.
    
    Renderiza la plantilla index.html que muestra en tiempo real:
    - La última placa detectada
    - Estado de la cita (si existe)
    - Información del cliente y vehículo
    - Estado de conexión con la cámara
    
    La plantilla utiliza JavaScript para actualizar los datos
    periódicamente mediante consultas AJAX al endpoint /datos.
    
    Returns:
        str: HTML renderizado de la página principal
    """
    return render_template('index.html')

@main_bp.route('/datos')
def datos():
    """
    Endpoint JSON que devuelve los datos actuales de la última consulta.
    
    Este endpoint es consultado periódicamente mediante AJAX desde
    la interfaz web para mantener la información actualizada sin
    necesidad de recargar la página. Proporciona:
    - Datos de la última placa detectada
    - Información de la cita correspondiente (si existe)
    - Estado actual de la conexión con la cámara
    
    Returns:
        Response: Objeto JSON con todos los datos actualizados
    """
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
    """
    Ruta para el panel de administración del sistema.
    
    Esta página permite a los administradores:
    - Ver el estado y configuración de la cámara
    - Consultar el historial completo de placas detectadas
    - Filtrar el historial por número de placa
    - Navegar por las diferentes páginas de resultados
    
    La función implementa paginación del lado del servidor para
    manejar eficientemente grandes volúmenes de registros.
    
    URL Parameters:
        pagina (int): Número de página a mostrar (predeterminado: 1)
        por_pagina (int): Cantidad de registros por página (predeterminado: 10)
        placa (str, opcional): Filtrar resultados por este número de placa
    
    Returns:
        str: HTML renderizado del panel de administración
    """
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
    """
    Endpoint para verificar el estado de conexión con la cámara.
    
    Este endpoint es utilizado para verificaciones periódicas del estado 
    de la cámara desde el panel de administración. Devuelve información
    sobre el estado actual de la conexión y la cantidad de eventos recientes.
    
    Returns:
        Response: Objeto JSON con información del estado de la cámara:
                  - estado: "Activo" o "Sin conexión"
                  - eventos_recientes: Cantidad de placas detectadas recientemente
                  - mensaje: Información detallada sobre el estado
    """
    conectado, mensaje = verificar_conexion_camara()
    placas = get_plates()
    estado = {
        "estado": "Activo" if conectado else "Sin conexión",
        "eventos_recientes": len(placas) if placas else 0,
        "mensaje": mensaje
    }
    return jsonify(estado) 
from datetime import datetime

# Estado compartido de la aplicación
ultima_consulta = {
    "placa": None,
    "fecha": None,
    "tiene_cita": False,
    "datos_cita": None,
    "mensaje": None,
    "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Conjunto para almacenar los eventos exactos ya procesados
eventos_exactos_procesados = set()

def crear_id_evento_exacto(placa, fecha):
    """Crea un ID único para un evento de detección de placa.
    
    Args:
        placa (str): Número de placa detectado
        fecha (datetime): Fecha y hora de la detección
        
    Returns:
        str: ID único para el evento
    """
    return f"{placa}_{fecha.strftime('%Y%m%d%H%M%S')}"

def actualizar_datos(resultado_cita, placa, fecha):
    """Actualiza los datos de última consulta con la información de la cita.
    
    Args:
        resultado_cita (dict): Resultado de la consulta a la API de citas
        placa (str): Número de placa consultado
        fecha (datetime): Fecha y hora de la detección
    """
    global ultima_consulta
    
    # Actualizar los datos para la web
    ultima_consulta["placa"] = placa
    ultima_consulta["fecha"] = fecha.strftime("%Y-%m-%d %H:%M:%S")
    ultima_consulta["actualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if resultado_cita and "codigo" in resultado_cita:
        if resultado_cita["codigo"] == "0" and resultado_cita["listadoDatosAgendamiento"]:
            cita = resultado_cita["listadoDatosAgendamiento"][0]
            ultima_consulta["tiene_cita"] = True
            ultima_consulta["datos_cita"] = cita
            ultima_consulta["mensaje"] = "CITA ENCONTRADA"
        else:
            ultima_consulta["tiene_cita"] = False
            ultima_consulta["datos_cita"] = None
            ultima_consulta["mensaje"] = resultado_cita.get("mensaje", "NO SE ENCONTRARON RESULTADOS")
    else:
        ultima_consulta["tiene_cita"] = False
        ultima_consulta["datos_cita"] = None
        ultima_consulta["mensaje"] = "ERROR DE CONEXIÓN" 
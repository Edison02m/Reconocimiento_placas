"""
Módulo de gestión del estado de la aplicación para el Sistema de Detección de Placas

Este módulo mantiene el estado global de la aplicación, almacenando información 
sobre la última detección de placa, los resultados de consulta de citas y 
el historial de eventos procesados. Proporciona funciones para:

1. Gestionar el estado actual de la última placa detectada
2. Actualizar los datos de cita correspondientes a un vehículo
3. Controlar qué eventos han sido procesados para evitar duplicación
4. Generar identificadores únicos para eventos de detección

El estado se mantiene en memoria durante la ejecución del programa y es
compartido entre los diferentes componentes de la aplicación.
"""

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
    """
    Crea un identificador único para un evento de detección de placa.
    
    Este identificador permite determinar si un evento específico ya ha sido
    procesado, evitando duplicados. Se compone del número de placa combinado
    con la fecha y hora exacta de detección, formateado como una cadena única.
    
    Args:
        placa (str): Número de placa detectado
        fecha (datetime): Fecha y hora de la detección
        
    Returns:
        str: Identificador único para el evento en formato "PLACA_YYYYMMDDHHMMSS"
    """
    return f"{placa}_{fecha.strftime('%Y%m%d%H%M%S')}"

def actualizar_datos(resultado_cita, placa, fecha):
    """
    Actualiza el estado global con los datos de la última consulta y cita.
    
    Esta función actualiza el diccionario global 'ultima_consulta' con la
    información de la placa detectada y el resultado de la consulta a la API
    de citas. Analiza la respuesta JSON de la API para determinar si el vehículo
    tiene una cita programada y extrae los datos relevantes.
    
    Args:
        resultado_cita (dict): Respuesta JSON de la API de citas o None si hubo error
        placa (str): Número de placa detectado
        fecha (datetime): Fecha y hora de la detección
        
    Returns:
        None: La función actualiza el estado global directamente
    """
    global ultima_consulta
    
    # Actualizar los datos básicos
    ultima_consulta["placa"] = placa
    ultima_consulta["fecha"] = fecha.strftime("%Y-%m-%d %H:%M:%S")
    ultima_consulta["actualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Si resultado_cita es None, establecer mensaje de error
    if resultado_cita is None:
        ultima_consulta["tiene_cita"] = False
        ultima_consulta["datos_cita"] = None
        ultima_consulta["mensaje"] = "ERROR DE CONEXIÓN"
        return
    
    # Si hay un mensaje de error, mostrarlo correctamente
    if isinstance(resultado_cita, dict) and "mensaje" in resultado_cita and resultado_cita.get("codigo") == "1":
        ultima_consulta["tiene_cita"] = False
        ultima_consulta["datos_cita"] = None
        ultima_consulta["mensaje"] = resultado_cita["mensaje"]
        return
    
    # Procesar respuesta normal
    if resultado_cita and "codigo" in resultado_cita:
        if resultado_cita["codigo"] == "0" and resultado_cita.get("listadoDatosAgendamiento", []):
            # Guardar la cita completa tal como viene de la API
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
        ultima_consulta["mensaje"] = "FORMATO DE RESPUESTA INVÁLIDO" 
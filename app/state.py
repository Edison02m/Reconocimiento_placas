"""Gestión del estado global de la aplicación"""

from datetime import datetime

ultima_consulta = {
    "placa": None,
    "fecha": None,
    "mensaje": None,
    "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

def actualizar_datos(placa, fecha, error=None):
    """Actualiza estado global con datos de última detección"""
    global ultima_consulta
    
    ultima_consulta["placa"] = placa
    ultima_consulta["fecha"] = fecha.strftime("%Y-%m-%d %H:%M:%S")
    ultima_consulta["actualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if error:
        ultima_consulta["mensaje"] = f"ERROR: {error}"
    else:
        ultima_consulta["mensaje"] = "PLACA DETECTADA Y ENVIADA" 
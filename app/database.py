"""
Módulo de gestión de datos para el Sistema de Detección de Placas

Maneja almacenamiento y recuperación de datos de placas vehiculares.
Diseñado para enviar datos a servidor remoto PHP/MySQL.
Base de datos local solo para diagnóstico.
"""

import requests
import os
from dotenv import load_dotenv
from app.config import COD_AGENCIA

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def enviar_placa_al_servidor(placa, fecha, hora, origen=COD_AGENCIA):
    """
    Envía datos de placa al servidor remoto vía HTTP POST.
    
    Args:
        placa (str): Número de placa detectado
        fecha (str): Fecha en formato YYYY-MM-DD
        hora (str): Hora en formato HH:MM:SS
        origen (str): Fuente de la detección
        
    Returns:
        tuple: (bool, str) - (éxito, mensaje)
    """
    # Dirección IP del servidor Windows Server desde variables de entorno
    base_url = os.getenv('REMOTE_SERVER_URL')
    url = f"{base_url}/insertar.php"
    
    # Datos a enviar
    data = {
        "placa": placa,
        "fecha": fecha,
        "hora": hora,
        "origen": origen
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        response.raise_for_status()  # Verificar si hay errores HTTP
        print(f" Placa {placa} enviada al servidor remoto")
        return True, response.text
    except requests.exceptions.RequestException as e:
        error_message = f"Error al enviar la placa al servidor: {e}"
        print(f" {error_message}")
        return False, error_message


def guardar_placa_en_db(placa, fecha, origen=COD_AGENCIA):
    """
    Punto de entrada para guardar placa en servidor remoto.
    Convierte datetime a formato texto para envío.
    
    Args:
        placa (str): Número de placa
        fecha (datetime): Fecha y hora de detección
        origen (str, optional): Código de agencia. Por defecto usa COD_AGENCIA del archivo de configuración.
        
    Returns:
        bool: Éxito de la operación
    """
    # Extraer fecha y hora por separado del objeto datetime
    fecha_str = fecha.strftime("%Y-%m-%d")
    hora_str = fecha.strftime("%H:%M:%S")
    
    # Enviar al servidor remoto únicamente
    exito, mensaje = enviar_placa_al_servidor(placa, fecha_str, hora_str, origen)
    return exito

def probar_conexion_servidor():
    """
    Prueba conexión al servidor remoto sin enviar datos.
    Utilizada durante el inicio del sistema.
    
    Returns:
        bool: Éxito de la conexión
    """
    print("\nProbando conexión al servidor remoto...")
    base_url = os.getenv('REMOTE_SERVER_URL')
    url = f"{base_url}/leer.php"
    
    try:
        # Solo verificar si podemos conectarnos al servidor
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        print(f" Conexión exitosa con el servidor remoto")
        print(f"   Código de estado: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f" No se pudo conectar con el servidor remoto")
        print(f"   Error: {e}")
        return False


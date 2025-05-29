"""
Módulo de consulta a la API de citas de Casabaca

Este módulo proporciona funcionalidad para consultar el sistema de citas
de Casabaca Toyota y verificar si un vehículo identificado por su placa
tiene una cita programada en el concesionario.

La consulta se realiza a través de un servicio web REST que devuelve 
información detallada de la cita (si existe) en formato JSON.
"""

import requests
import json
from app.config import URL_CITAS, NO_CIA, COD_AGENCIA

def consultar_cita(placa):
    """
    Consulta si un vehículo tiene una cita programada en Casabaca.
    
    Realiza una petición HTTP GET a la API de citas de Casabaca 
    utilizando el número de placa como parámetro de búsqueda, junto
    con el número de compañía y código de agencia configurados.
    
    La respuesta de la API incluye datos como:
    - Información del cliente (nombre, cédula)
    - Fecha y hora de la cita
    - Información del vehículo
    - Datos del asesor asignado
    - Número de orden
    
    Args:
        placa (str): Número de placa del vehículo a consultar
        
    Returns:
        dict: Respuesta JSON de la API de citas con toda la información
              de la cita programada, o un dict con error si hay problemas
              en la consulta o el vehículo no tiene cita
    """
    try:
        params = {
            "noCia": NO_CIA,
            "placa": placa,
            "codAgencia": COD_AGENCIA
        }
        response = requests.get(URL_CITAS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio de citas: {e}")
        return {"codigo": "1", "mensaje": f"Error al conectar con el servicio de citas"}
    except json.JSONDecodeError as e:
        print(f"Error al procesar la respuesta del servicio: {e}")
        return {"codigo": "1", "mensaje": "Error al procesar la respuesta del servicio"}
    except Exception as e:
        error_str = str(e)
        # Si es un error de PostgreSQL, mostrar un mensaje genérico
        if "postgres" in error_str.lower() or "psycopg" in error_str.lower():
            print(f"Error al consultar la base de datos del servidor")
            return {"codigo": "1", "mensaje": "Error al consultar la base de datos del servidor"}
        else:
            print(f"Error desconocido al consultar cita: {e}")
            return {"codigo": "1", "mensaje": f"Error al consultar información de cita"} 
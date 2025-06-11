"""
Módulo de consulta a la API de citas 

Servicio web REST para verificar citas programadas por placa.
"""

import requests
import json
from app.config import URL_CITAS, NO_CIA, AGENCIA

def consultar_cita(placa):
    """
    Consulta cita programada por número de placa.
    
    Args:
        placa (str): Número de placa del vehículo
        
    Returns:
        dict: Datos de la cita o dict con error
    """
    try:
        params = {
            "noCia": NO_CIA,
            "placa": placa,
            "agencia": AGENCIA
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
        if "postgres" in error_str.lower() or "psycopg" in error_str.lower():
            print(f"Error al consultar la base de datos del servidor")
            return {"codigo": "1", "mensaje": "Error al consultar la base de datos del servidor"}
        else:
            print(f"Error desconocido al consultar cita: {e}")
            return {"codigo": "1", "mensaje": f"Error al consultar información de cita"} 
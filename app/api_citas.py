import requests
from app.config import URL_CITAS, NO_CIA, COD_AGENCIA

def consultar_cita(placa):
    """Consulta si la placa tiene una cita programada.
    
    Args:
        placa (str): Número de placa a consultar
        
    Returns:
        dict: Respuesta JSON de la API de citas o None si hay error
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
    except Exception:
        return None 
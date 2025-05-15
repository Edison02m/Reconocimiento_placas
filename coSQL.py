import requests

def enviar_datos_placa(placa, fecha, hora, origen="camara1"):
    """
    Envía los datos de una placa detectada al servidor.
    
    Args:
        placa (str): Número de placa detectado
        fecha (str): Fecha en formato YYYY-MM-DD
        hora (str): Hora en formato HH:MM:SS
        origen (str): Origen de la detección (opcional)
        
    Returns:
        bool: True si se envió correctamente, False en caso contrario
        str: Mensaje del servidor o error
    """
    # Dirección IP de tu servidor Windows Server
    url = "http://192.168.20.200/insertar.php"
    
    # Datos que deseas enviar
    data = {
        "placa": placa,
        "fecha": fecha,
        "hora": hora,
        "origen": origen
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        response.raise_for_status()  # Verificar si hay errores HTTP
        return True, response.text
    except requests.exceptions.RequestException as e:
        error_message = f"Error al enviar la solicitud: {e}"
        print(error_message)
        return False, error_message

# Ejemplo de uso
if __name__ == "__main__":
    exito, mensaje = enviar_datos_placa("ABC123", "2025-05-15", "13:45:00")
    if exito:
        print("Datos enviados correctamente")
        print("Respuesta del servidor:", mensaje)
    else:
        print("Error:", mensaje)
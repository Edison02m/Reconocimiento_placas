import mysql.connector
from mysql.connector import Error
from datetime import datetime
import requests
from app.config import DB_CONFIG

def conectar_db():
    """Establece y retorna una conexión a la base de datos MySQL.
    Nota: Esta función se mantiene para verificar la conexión pero no se usa para almacenar datos."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def enviar_placa_al_servidor(placa, fecha, hora, origen="Cámara IP"):
    """Envía los datos de una placa detectada al servidor remoto.
    
    Args:
        placa (str): Número de placa detectado
        fecha (str): Fecha en formato YYYY-MM-DD
        hora (str): Hora en formato HH:MM:SS
        origen (str): Fuente de la detección
        
    Returns:
        bool: True si se envió correctamente, False en caso contrario
        str: Mensaje del servidor o error
    """
    # Dirección IP del servidor Windows Server
    url = "http://192.168.20.200/insertar.php"
    
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
        print(f"✅ Placa {placa} enviada al servidor remoto")
        return True, response.text
    except requests.exceptions.RequestException as e:
        error_message = f"Error al enviar la placa al servidor: {e}"
        print(f"❌ {error_message}")
        return False, error_message

def obtener_historial_placas(pagina=1, registros_por_pagina=10, filtro_placa=None):
    """Obtiene el historial de placas detectadas desde el servidor remoto con paginación.
    
    Args:
        pagina (int): Número de página a mostrar (iniciando en 1)
        registros_por_pagina (int): Cantidad de registros por página
        filtro_placa (str, opcional): Filtrar por número de placa
        
    Returns:
        dict: Diccionario con los registros paginados y metadatos de paginación
    """
    url = "http://192.168.20.200/leer.php"
    
    # Parámetros para la paginación (si el servidor lo soporta)
    params = {}
    if filtro_placa:
        params['placa'] = filtro_placa
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        # Intentar parsear la respuesta como JSON
        try:
            # Obtener todos los registros
            todos_registros = response.json()
            
            # Asegurarse de que todos los registros tienen los campos necesarios
            for registro in todos_registros:
                # Asegurar que los campos obligatorios existen
                registro['placa'] = registro.get('placa', 'N/A')
                registro['fecha'] = registro.get('fecha', 'N/A')
                registro['hora'] = registro.get('hora', 'N/A')
                registro['origen'] = registro.get('origen', 'Desconocido')
                # El campo fecha_registro puede no existir en algunos registros
                if 'fecha_registro' not in registro:
                    registro['fecha_registro'] = registro.get('fecha', '') + ' ' + registro.get('hora', '')
            
            # Cantidad total de registros
            total_registros = len(todos_registros)
            
            # Calcular el total de páginas
            total_paginas = max(1, (total_registros + registros_por_pagina - 1) // registros_por_pagina)
            
            # Asegurar que la página solicitada existe
            if pagina < 1:
                pagina = 1
            elif pagina > total_paginas and total_paginas > 0:
                pagina = total_paginas
            
            # Calcular inicio y fin para la paginación
            inicio = (pagina - 1) * registros_por_pagina
            fin = min(inicio + registros_por_pagina, total_registros)
            
            # Extraer solo los registros de la página actual
            registros_pagina = todos_registros[inicio:fin] if total_registros > 0 else []
            
            print(f"✅ Se obtuvieron {len(registros_pagina)} de {total_registros} registros (página {pagina} de {total_paginas})")
            
            # Devolver los datos con metadatos de paginación
            return {
                "registros": registros_pagina,
                "total_registros": total_registros,
                "total_paginas": total_paginas,
                "pagina_actual": pagina,
                "registros_por_pagina": registros_por_pagina
            }
            
        except ValueError:
            print("❌ Error: El servidor no devolvió un formato JSON válido")
            print(f"Respuesta recibida: {response.text[:100]}...")  # Mostrar parte de la respuesta
            return {
                "registros": [],
                "total_registros": 0,
                "total_paginas": 0,
                "pagina_actual": 1,
                "registros_por_pagina": registros_por_pagina,
                "error": "Formato de respuesta inválido"
            }
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al obtener el historial del servidor: {e}"
        print(f"❌ {error_msg}")
        return {
            "registros": [],
            "total_registros": 0,
            "total_paginas": 0,
            "pagina_actual": 1,
            "registros_por_pagina": registros_por_pagina,
            "error": error_msg
        }

def guardar_placa_en_db(placa, fecha, origen="Cámara IP"):
    """Guarda un registro de placa detectada en el servidor remoto.
    
    Args:
        placa (str): Número de placa detectado
        fecha (datetime): Fecha y hora de la detección
        origen (str): Fuente de la detección. Por defecto "Cámara IP"
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    # Extraer fecha y hora por separado del objeto datetime
    fecha_str = fecha.strftime("%Y-%m-%d")
    hora_str = fecha.strftime("%H:%M:%S")
    
    # Enviar al servidor remoto únicamente
    exito, mensaje = enviar_placa_al_servidor(placa, fecha_str, hora_str, origen)
    return exito

def probar_conexion_servidor():
    """Prueba la conexión con el servidor remoto."""
    print("\nProbando conexión al servidor remoto...")
    prueba_placa = "TEST123"
    prueba_fecha = datetime.now().strftime("%Y-%m-%d")
    prueba_hora = datetime.now().strftime("%H:%M:%S")
    
    exito, mensaje = enviar_placa_al_servidor(prueba_placa, prueba_fecha, prueba_hora, "Prueba")
    
    if exito:
        print(f"✅ Conexión exitosa con el servidor remoto")
        print(f"   Respuesta: {mensaje}")
    else:
        print(f"❌ No se pudo conectar con el servidor remoto")
        print(f"   Error: {mensaje}")
        
    return exito

if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, probar las conexiones
    print("=== PRUEBA DE CONEXIONES ===")
    
    # Probar conexión al servidor remoto
    if probar_conexion_servidor():
        # Obtener historial
        print("\nObteniendo historial de placas (paginado)...")
        
        # Mostrar primera página
        resultado = obtener_historial_placas(pagina=1, registros_por_pagina=5)
        if resultado["registros"]:
            print(f"Página {resultado['pagina_actual']} de {resultado['total_paginas']} (Total: {resultado['total_registros']} registros)")
            for i, registro in enumerate(resultado["registros"]):
                print(f"{i+1}. Placa: {registro.get('placa', 'N/A')}, "
                      f"Fecha: {registro.get('fecha', 'N/A')}, "
                      f"Hora: {registro.get('hora', 'N/A')}") 
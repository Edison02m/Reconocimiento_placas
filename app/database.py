"""
Módulo de gestión de datos para el Sistema de Detección de Placas

Este módulo maneja todas las operaciones relacionadas con el almacenamiento
y recuperación de datos de placas vehiculares detectadas. Proporciona funciones para:

1. Conectarse a una base de datos MySQL local (solo para diagnóstico)
2. Enviar los datos de placas detectadas a un servidor remoto
3. Recuperar el historial de detecciones con capacidades de paginación y filtrado
4. Probar la conectividad con el servidor remoto

El sistema está diseñado para enviar todos los datos al servidor remoto (PHP/MySQL),
manteniendo la base de datos local solo para propósitos de diagnóstico.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import requests
from app.config import DB_CONFIG

def conectar_db():
    """
    Establece y retorna una conexión a la base de datos MySQL local.
    
    Esta función se mantiene principalmente para verificar la conexión durante
    el diagnóstico del sistema. En la operación normal, los datos se envían
    directamente al servidor remoto y no se almacenan localmente.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Objeto de conexión a MySQL 
                                                   o None si hay error
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def enviar_placa_al_servidor(placa, fecha, hora, origen="Cámara IP"):
    """
    Envía los datos de una placa detectada al servidor remoto.
    
    Realiza una petición HTTP POST al servidor remoto (PHP) para almacenar
    la información de una placa detectada. Esta es la función principal
    para el almacenamiento de datos en el sistema.
    
    Args:
        placa (str): Número de placa detectado
        fecha (str): Fecha en formato YYYY-MM-DD
        hora (str): Hora en formato HH:MM:SS
        origen (str): Fuente de la detección (por defecto "Cámara IP")
        
    Returns:
        tuple: (bool, str) - (True/False si se envió correctamente, 
                             Mensaje del servidor o descripción del error)
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
    """
    Obtiene el historial de placas detectadas desde el servidor remoto con paginación.
    
    Recupera los registros de placas detectadas almacenados en el servidor remoto,
    implementando capacidades de paginación y filtrado. Esta función es utilizada
    principalmente por el panel de administración para mostrar el historial.
    
    Args:
        pagina (int): Número de página a mostrar (iniciando en 1)
        registros_por_pagina (int): Cantidad de registros por página
        filtro_placa (str, opcional): Filtrar resultados por número de placa
        
    Returns:
        dict: Diccionario con los siguientes campos:
            - registros: Lista de diccionarios con los datos de las placas
            - total_registros: Cantidad total de registros disponibles
            - total_paginas: Número total de páginas
            - pagina_actual: Número de página actual
            - registros_por_pagina: Cantidad de registros por página
            - error: Mensaje de error (solo presente si hay un error)
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
            
            # Filtrar registros vacíos o inválidos antes de procesar
            todos_registros = [reg for reg in todos_registros if isinstance(reg, dict) and reg]
            
            # Asegurarse de que todos los registros tienen los campos necesarios
            for registro in todos_registros:
                # Asegurar que los campos obligatorios existen y no están vacíos
                registro['placa'] = registro.get('placa') or 'N/A'
                registro['fecha'] = registro.get('fecha') or 'N/A'
                registro['hora'] = registro.get('hora') or 'N/A'
                registro['origen'] = registro.get('origen') or 'Desconocido'
                
                # El campo fecha_registro puede no existir en algunos registros
                if not registro.get('fecha_registro'):
                    fecha_str = registro.get('fecha', '')
                    hora_str = registro.get('hora', '')
                    registro['fecha_registro'] = f"{fecha_str} {hora_str}".strip()
                    # Si sigue vacío, usar un valor predeterminado
                    if not registro['fecha_registro']:
                        registro['fecha_registro'] = 'N/A'
            
            # Eliminar registros que todavía tienen campos obligatorios vacíos
            todos_registros = [reg for reg in todos_registros if 
                              reg.get('placa') != 'N/A' or 
                              (reg.get('fecha') != 'N/A' and reg.get('hora') != 'N/A')]
            
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
            
            print(f"✅ Se obtuvieron {len(registros_pagina)} de {total_registros} registros válidos (página {pagina} de {total_paginas})")
            
            # Devolver los datos con metadatos de paginación
            return {
                "registros": registros_pagina,
                "total_registros": total_registros,
                "total_paginas": total_paginas,
                "pagina_actual": pagina,
                "registros_por_pagina": registros_por_pagina
            }
            
        except ValueError as e:
            print(f"❌ Error al procesar JSON: {e}")
            print(f"Respuesta recibida: {response.text[:100]}...")  # Mostrar parte de la respuesta
            return {
                "registros": [],
                "total_registros": 0,
                "total_paginas": 0,
                "pagina_actual": 1,
                "registros_por_pagina": registros_por_pagina,
                "error": f"Formato de respuesta inválido: {str(e)}"
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
    """
    Guarda un registro de placa detectada en el servidor remoto.
    
    Esta función actúa como punto de entrada principal para guardar
    los datos de una nueva placa detectada. Convierte el objeto datetime
    en formato de texto adecuado y envía los datos al servidor remoto.
    
    Args:
        placa (str): Número de placa detectado
        fecha (datetime): Objeto datetime con la fecha y hora de la detección
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
    """
    Prueba la conexión con el servidor remoto de almacenamiento.
    
    Verifica si el servidor remoto está accesible sin enviar datos de prueba.
    Esta función se utiliza principalmente durante el inicio del sistema
    para comprobar la disponibilidad del servidor de almacenamiento.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    print("\nProbando conexión al servidor remoto...")
    url = "http://192.168.20.200/leer.php"
    
    try:
        # Solo verificar si podemos conectarnos al servidor
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        print(f"✅ Conexión exitosa con el servidor remoto")
        print(f"   Código de estado: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo conectar con el servidor remoto")
        print(f"   Error: {e}")
        return False

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
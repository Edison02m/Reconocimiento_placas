"""
Módulo de gestión de datos para el Sistema de Detección de Placas

Maneja almacenamiento y recuperación de datos de placas vehiculares.
Diseñado para enviar datos a servidor remoto PHP/MySQL.
Base de datos local solo para diagnóstico.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from app.config import DB_CONFIG

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def conectar_db():
    """
    Establece conexión a la base de datos MySQL local (solo diagnóstico).
    
    Returns:
        mysql.connector.connection.MySQLConnection o None si hay error
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def enviar_placa_al_servidor(placa, fecha, hora, origen="Cámara IP"):
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
        print(f"✅ Placa {placa} enviada al servidor remoto")
        return True, response.text
    except requests.exceptions.RequestException as e:
        error_message = f"Error al enviar la placa al servidor: {e}"
        print(f"❌ {error_message}")
        return False, error_message

def obtener_historial_placas(pagina=1, registros_por_pagina=10, filtro_placa=None):
    """
    Obtiene historial de placas desde servidor remoto con paginación.
    
    Args:
        pagina (int): Número de página (desde 1)
        registros_por_pagina (int): Cantidad de registros por página
        filtro_placa (str, opcional): Filtro por número de placa
        
    Returns:
        dict: Con registros, metadatos de paginación y posible error
    """
    base_url = os.getenv('REMOTE_SERVER_URL')
    url = f"{base_url}/leer.php"
    
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
    Punto de entrada para guardar placa en servidor remoto.
    Convierte datetime a formato texto para envío.
    
    Args:
        placa (str): Número de placa
        fecha (datetime): Fecha y hora de detección
        origen (str): Fuente de detección
        
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
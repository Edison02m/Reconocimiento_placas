"""
Módulo de comunicación con la cámara Hikvision para detección de placas vehiculares

Este módulo contiene las funciones necesarias para establecer comunicación con 
la cámara IP Hikvision que realiza la detección de placas vehiculares. Implementa
métodos para verificar la conexión, obtener las placas detectadas y procesar la
información recibida.

La cámara expone una API REST que devuelve datos en formato XML, los cuales son
procesados para extraer la información relevante de las placas detectadas.
"""

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import time
from app.config import URL, USERNAME, PASSWORD, HEADERS, BODY_XML

def verificar_conexion_camara():
    """
    Verifica si hay conexión con la cámara Hikvision.
    
    Realiza una solicitud de prueba a la API de la cámara para comprobar
    si está disponible y responde correctamente. Maneja diferentes tipos de
    errores que pueden ocurrir durante la comunicación.
    
    Returns:
        tuple: (bool, str) - (True/False si hay conexión, mensaje descriptivo)
    """
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            data=BODY_XML.encode('utf-8'),
            auth=HTTPDigestAuth(USERNAME, PASSWORD),
            timeout=5  # Reducido para hacer la verificación más rápida
        )
        response.raise_for_status()
        return True, "Conexión exitosa con la cámara"
    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con la cámara (Error de conexión)"
    except requests.exceptions.Timeout:
        return False, "Tiempo de espera agotado al conectar con la cámara"
    except requests.exceptions.HTTPError as e:
        return False, f"Error HTTP al conectar con la cámara: {e}"
    except Exception as e:
        return False, f"Error desconocido al conectar con la cámara: {e}"

def get_plates():
    """
    Obtiene las placas detectadas por la cámara Hikvision.
    
    Consulta la API de la cámara para obtener los registros de placas vehiculares
    detectadas, procesa la respuesta XML y extrae la información relevante.
    Los resultados se ordenan por fecha de detección (más reciente primero).
    
    El método maneja correctamente el namespace XML que puede variar según la
    versión del firmware de la cámara, y procesa las fechas para convertirlas
    a objetos datetime de Python.
    
    Returns:
        list: Lista de diccionarios con información de las placas detectadas.
              Cada diccionario contiene 'placa', 'fecha' y 'país'.
              Si hay error de conexión o proceso, devuelve lista vacía.
    """
    conectado, _ = verificar_conexion_camara()
    if not conectado:
        return []
        
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            data=BODY_XML.encode('utf-8'),
            auth=HTTPDigestAuth(USERNAME, PASSWORD),
            timeout=10
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        plates = []

        # Detectar el namespace correcto del XML
        namespace = root.tag.split('}')[0].strip('{') if '}' in root.tag else None
        ns = {'ns': namespace} if namespace else None

        # Buscar todas las placas
        xpath = ".//ns:Plate" if namespace else ".//Plate"
        for plate in root.findall(xpath, ns):
            # Función auxiliar para obtener texto con o sin namespace
            def get_text(element, tag):
                return (element.findtext(f"ns:{tag}", namespaces=ns) if namespace 
                       else element.findtext(tag))

            plate_number = get_text(plate, "plateNumber")
            capture_time = get_text(plate, "captureTime")
            country = get_text(plate, "country")

            if plate_number and capture_time:
                # Convertir el formato de hora a uno que Python pueda entender
                capture_time = capture_time.replace("-500", "-0500")
                try:
                    dt = datetime.strptime(capture_time, "%Y%m%dT%H%M%S%z")
                    if plate_number.lower() != "unknown":
                        plates.append({
                            "placa": plate_number,
                            "fecha": dt,
                            "país": country
                        })
                except ValueError:
                    continue

        plates.sort(key=lambda x: x["fecha"], reverse=True)
        return plates

    except Exception:
        # Devolver lista vacía en caso de error
        return []

def probar_conexion():
    """
    Función de diagnóstico para probar la conexión con la cámara desde línea de comandos.
    
    Imprime información detallada sobre el resultado de la conexión, incluyendo:
    - Tiempo de respuesta
    - Estado de la conexión
    - Cantidad de placas detectadas
    - Últimas 3 placas detectadas (si existen)
    - Sugerencias en caso de error
    
    Esta función está diseñada para ser utilizada directamente cuando se ejecuta
    este archivo como script principal.
    """
    print(f"Probando conexión a la cámara en: {URL}")
    print(f"Usuario: {USERNAME}")
    
    inicio = time.time()
    conectado, mensaje = verificar_conexion_camara()
    tiempo = time.time() - inicio
    
    print(f"Tiempo de respuesta: {tiempo:.2f} segundos")
    
    if conectado:
        print("✅ CONEXIÓN EXITOSA")
        placas = get_plates()
        print(f"Se encontraron {len(placas)} registros de placas")
        if placas:
            print("\nÚltimas 3 placas detectadas:")
            for i, placa in enumerate(placas[:3]):
                print(f"{i+1}. Placa: {placa['placa']}, Fecha: {placa['fecha']}")
    else:
        print(f"❌ ERROR DE CONEXIÓN: {mensaje}")
        print("\nVerifique:")
        print("1. Que la cámara esté encendida y conectada a la red")
        print("2. Que la URL configurada sea correcta")
        print("3. Que las credenciales sean válidas")
        print("4. Que no haya restricciones de firewall bloqueando la conexión")

if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, probar la conexión
    probar_conexion() 
"""
Módulo de comunicación con la cámara Hikvision para detección de placas vehiculares

API REST que devuelve datos en formato XML. Requiere autenticación HTTP Digest.
"""

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import time
from app.config import URL, USERNAME, PASSWORD, HEADERS, BODY_XML

def verificar_conexion_camara():
    """
    Verifica conexión con la cámara Hikvision.
    
    Returns:
        tuple: (bool, str) - (True/False si hay conexión, mensaje descriptivo)
    """
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            data=BODY_XML.encode('utf-8'),
            auth=HTTPDigestAuth(USERNAME, PASSWORD),
            timeout=5 
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
    
    Maneja namespace XML variable según versión del firmware.
    Resultados ordenados por fecha (más reciente primero).
    
    Returns:
        list: Diccionarios con 'placa', 'fecha' y 'país'.
              Lista vacía si hay error.
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

        namespace = root.tag.split('}')[0].strip('{') if '}' in root.tag else None
        ns = {'ns': namespace} if namespace else None

        xpath = ".//ns:Plate" if namespace else ".//Plate"
        for plate in root.findall(xpath, ns):
            def get_text(element, tag):
                return (element.findtext(f"ns:{tag}", namespaces=ns) if namespace 
                       else element.findtext(tag))

            plate_number = get_text(plate, "plateNumber")
            capture_time = get_text(plate, "captureTime")
            country = get_text(plate, "country")

            if plate_number and capture_time:
                capture_time = capture_time.replace("-500", "-0500")
                
                import re
                plate_number_cleaned = re.sub(r'[^A-Za-z0-9]', '', plate_number)
                
                try:
                    dt = datetime.strptime(capture_time, "%Y%m%dT%H%M%S%z")
                    if plate_number_cleaned.lower() != "unknown" and plate_number_cleaned:
                        plates.append({
                            "placa": plate_number_cleaned,
                            "fecha": dt,
                            "país": country
                        })
                except ValueError:
                    continue

        plates.sort(key=lambda x: x["fecha"], reverse=True)
        return plates

    except Exception:
        return []

def probar_conexion():
    """
    Función de diagnóstico para probar la conexión con la cámara.
    Para uso cuando se ejecuta este archivo como script principal.
    """
    print(f"Probando conexión a la cámara en: {URL}")
    print(f"Usuario: {USERNAME}")
    
    inicio = time.time()
    conectado, mensaje = verificar_conexion_camara()
    tiempo = time.time() - inicio
    
    print(f"Tiempo de respuesta: {tiempo:.2f} segundos")
    
    if conectado:
        print(" CONEXIÓN EXITOSA")
        placas = get_plates()
        print(f"Se encontraron {len(placas)} registros de placas")
        if placas:
            print("\nÚltimas 3 placas detectadas:")
            for i, placa in enumerate(placas[:3]):
                print(f"{i+1}. Placa: {placa['placa']}, Fecha: {placa['fecha']}")
    else:
        print(f" ERROR DE CONEXIÓN: {mensaje}")

if __name__ == "__main__":
    probar_conexion() 
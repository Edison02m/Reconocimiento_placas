"""
Módulo de monitoreo continuo para la detección de placas vehiculares

Este módulo implementa un sistema de monitoreo en segundo plano que verifica
continuamente si hay nuevas placas detectadas por la cámara. Cuando detecta
una nueva placa, realiza las siguientes acciones:

1. Consulta si el vehículo tiene citas programadas
2. Actualiza el estado del sistema para mostrar la información en la consola
"""

import time
import threading
from app.camera import get_plates
from app.api_citas import consultar_cita
from app.state import actualizar_datos, crear_id_evento_exacto, eventos_exactos_procesados, ultima_consulta
from app.config import INTERVALO_CONSULTA

def procesar_ultimo_evento():
    """
    Procesa el evento más reciente de detección de placa.
    
    Esta función realiza el flujo principal de procesamiento cuando se detecta
    una nueva placa:
    1. Obtiene la lista de placas detectadas recientemente
    2. Verifica si la placa más reciente ya ha sido procesada (evita duplicados)
    3. Consulta si el vehículo tiene una cita programada
    4. Actualiza el estado del sistema para mostrar la información en la consola
    5. Marca el evento como procesado para evitar procesarlo nuevamente
    
    Si no hay placas detectadas o la última ya fue procesada, la función
    termina sin realizar ninguna acción.
    
    Returns:
        None
    """
    try:
        placas = get_plates()
        if not placas:
            return

        ultimo_evento = placas[0]
        id_evento_exacto = crear_id_evento_exacto(ultimo_evento["placa"], ultimo_evento["fecha"])
        
        if id_evento_exacto not in eventos_exactos_procesados:
            try:
                resultado_cita = consultar_cita(ultimo_evento["placa"])
                actualizar_datos(resultado_cita, ultimo_evento["placa"], ultimo_evento["fecha"])
            except Exception as e:
                print(f"Error al consultar cita: {e}")
                datos_error = {
                    "codigo": "1",
                    "mensaje": f"Error al consultar información: {str(e)[:100]}"
                }
                actualizar_datos(datos_error, ultimo_evento["placa"], ultimo_evento["fecha"])
            eventos_exactos_procesados.add(id_evento_exacto)
    except Exception as e:
        print(f"Error general en el procesamiento de evento: {e}")

def monitor_thread():
    """
    Función que se ejecuta en un hilo separado para monitorear continuamente la cámara.
    
    Este procedimiento implementa el bucle infinito de monitoreo que verifica
    periódicamente si hay nuevas placas detectadas. El intervalo entre consultas
    se configura mediante la constante INTERVALO_CONSULTA en el archivo config.py.
    
    El bucle continuará indefinidamente hasta que el programa principal termine,
    ya que se ejecuta como un hilo daemon.
    
    Returns:
        None
    """
    while True:
        try:
            procesar_ultimo_evento()
        except Exception as e:
            print(f"Error en el hilo de monitoreo: {e}")
        time.sleep(INTERVALO_CONSULTA)

def iniciar_monitor():
    """
    Inicia el hilo de monitoreo en segundo plano.
    
    Crea y arranca un nuevo hilo (Thread) que ejecuta la función monitor_thread
    en segundo plano. El hilo se configura como daemon para que termine 
    automáticamente cuando el programa principal finalice.
    
    Returns:
        threading.Thread: Objeto Thread que representa el hilo de monitoreo iniciado
    """
    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    return t

def obtener_ultima_deteccion():
    """
    Obtiene la información de la última placa detectada.
    
    Esta función devuelve la información actualizada sobre la última placa
    detectada por el sistema, incluyendo datos sobre la cita si existe.
    
    Returns:
        dict: Diccionario con los datos de la última detección o None si no hay datos
    """
    if ultima_consulta["placa"] is None:
        return None
    return ultima_consulta 
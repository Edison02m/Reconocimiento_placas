"""
Módulo de monitoreo continuo para la detección de placas vehiculares

Este módulo implementa un sistema de monitoreo en segundo plano que verifica
continuamente si hay nuevas placas detectadas por la cámara. Cuando detecta
una nueva placa, realiza las siguientes acciones:

1. Almacena la información de la placa en el servidor remoto
2. Consulta si el vehículo tiene citas programadas
3. Actualiza el estado del sistema para mostrar la información en la interfaz web

El monitoreo se ejecuta en un hilo separado (daemon thread) para no bloquear
la aplicación principal mientras realiza estas tareas.
"""

import time
import threading
from app.camera import get_plates
from app.api_citas import consultar_cita
from app.database import guardar_placa_en_db
from app.state import actualizar_datos, crear_id_evento_exacto, eventos_exactos_procesados
from app.config import INTERVALO_CONSULTA

def procesar_ultimo_evento():
    """
    Procesa el evento más reciente de detección de placa.
    
    Esta función realiza el flujo principal de procesamiento cuando se detecta
    una nueva placa:
    1. Obtiene la lista de placas detectadas recientemente
    2. Verifica si la placa más reciente ya ha sido procesada (evita duplicados)
    3. Guarda la información de la placa en la base de datos
    4. Consulta si el vehículo tiene una cita programada
    5. Actualiza el estado del sistema para mostrar la información en la web
    6. Marca el evento como procesado para evitar procesarlo nuevamente
    
    Si no hay placas detectadas o la última ya fue procesada, la función
    termina sin realizar ninguna acción.
    
    Returns:
        None
    """
    placas = get_plates()
    if not placas:
        return

    ultimo_evento = placas[0]
    id_evento_exacto = crear_id_evento_exacto(ultimo_evento["placa"], ultimo_evento["fecha"])
    
    if id_evento_exacto not in eventos_exactos_procesados:
        # Guardar la placa en la base de datos
        guardar_placa_en_db(ultimo_evento["placa"], ultimo_evento["fecha"])
        
        # Consultar cita y actualizar datos para la web
        resultado_cita = consultar_cita(ultimo_evento["placa"])
        actualizar_datos(resultado_cita, ultimo_evento["placa"], ultimo_evento["fecha"])
        
        # Marcar como procesado
        eventos_exactos_procesados.add(id_evento_exacto)

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
        procesar_ultimo_evento()
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
"""Monitoreo continuo de placas detectadas por la cámara"""

import time
import threading
from app.camera import get_plates
from app.state import actualizar_datos, ultima_consulta
from app.config import INTERVALO_CONSULTA
from app.supabase_client import enviar_deteccion_a_supabase

ultimo_evento_procesado = None

def procesar_ultimo_evento():
    """Procesa evento más reciente: obtiene placas, envía a Supabase si es nueva, actualiza estado"""
    global ultimo_evento_procesado
    
    try:
        placas = get_plates()
        if not placas:
            return

        ultimo_evento = placas[0]
        
        evento_actual = f"{ultimo_evento['placa']}_{ultimo_evento['fecha'].strftime('%Y%m%d%H%M%S')}"
        
        if evento_actual != ultimo_evento_procesado:
            try:
                actualizar_datos(ultimo_evento["placa"], ultimo_evento["fecha"])
                enviar_deteccion_a_supabase(ultimo_evento["placa"])
                
            except Exception as e:
                print(f"Error al procesar placa: {e}")
                actualizar_datos(ultimo_evento["placa"], ultimo_evento["fecha"], error=str(e))
            
            ultimo_evento_procesado = evento_actual
    except Exception as e:
        print(f"Error general en el procesamiento de evento: {e}")

def monitor_thread():
    """Bucle infinito de monitoreo ejecutado en hilo daemon"""
    while True:
        try:
            procesar_ultimo_evento()
        except Exception as e:
            print(f"Error en el hilo de monitoreo: {e}")
        time.sleep(INTERVALO_CONSULTA)

def iniciar_monitor():
    """Inicia hilo daemon de monitoreo en segundo plano"""
    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    return t

def obtener_ultima_deteccion():
    """Retorna dict con datos de última detección o None"""
    if ultima_consulta["placa"] is None:
        return None
    return ultima_consulta 
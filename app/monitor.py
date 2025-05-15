import time
import threading
from app.camera import get_plates
from app.api_citas import consultar_cita
from app.database import guardar_placa_en_db
from app.state import actualizar_datos, crear_id_evento_exacto, eventos_exactos_procesados
from app.config import INTERVALO_CONSULTA

def procesar_ultimo_evento():
    """Procesa el evento más reciente de detección de placa."""
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
    """Función que se ejecuta en un hilo separado para monitorear continuamente la cámara."""
    while True:
        procesar_ultimo_evento()
        time.sleep(INTERVALO_CONSULTA)

def iniciar_monitor():
    """Inicia el hilo de monitoreo en segundo plano."""
    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    return t 
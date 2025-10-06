"""
Módulo ultra-optimizado de integración con Supabase para detecciones de placas

Solo contiene la función esencial para envío rápido de placas.
La verificación de conexión se hace una sola vez en run.py
"""

from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

# Crear cliente de Supabase una sola vez
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def enviar_deteccion_a_supabase(placa):
    """
    Envía una detección de placa a Supabase de forma rápida.
    
    Args:
        placa (str): Número de placa detectado
        
    Returns:
        bool: True si se envió correctamente, False en caso de error
    """
    try:
        # Envío directo sin verificaciones para máxima velocidad
        supabase.table("detecciones").insert({"placa": placa}).execute()
        return True
    except Exception:
        # Silenciar errores para no afectar el flujo principal
        return False

def verificar_conexion_supabase_inicial():
    """
    Verificación inicial de conexión con Supabase (solo para uso en run.py).
    
    Returns:
        tuple: (bool, str) - (True/False si hay conexión, mensaje)
    """
    try:
        supabase.table("detecciones").select("id").limit(1).execute()
        return True, "Conexión exitosa con Supabase"
    except Exception as e:
        return False, f"Error al conectar con Supabase: {e}"
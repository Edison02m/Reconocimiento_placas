"""Cliente Supabase optimizado con HTTP pooling y count='none'"""

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from app.config import SUPABASE_URL, SUPABASE_KEY
import httpx

http_client = httpx.Client(
    timeout=5.0,
    limits=httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10,
        keepalive_expiry=30
    )
)

options = ClientOptions(
    auto_refresh_token=False,
    persist_session=False
)

supabase: Client = create_client(
    SUPABASE_URL, 
    SUPABASE_KEY,
    options=options
)

def enviar_deteccion_a_supabase(placa):
    """Envía detección a Supabase con count='none'"""
    try:
        supabase.table("detecciones").insert(
            {"placa": placa},
            count="none"
        ).execute()
        return True
    except Exception:
        return False

def verificar_conexion_supabase_inicial():
    """Verificación inicial de conexión (solo para run.py)"""
    try:
        supabase.table("detecciones").select("id").limit(1).execute()
        return True, "Conexión exitosa con Supabase"
    except Exception as e:
        return False, f"Error al conectar con Supabase: {e}"
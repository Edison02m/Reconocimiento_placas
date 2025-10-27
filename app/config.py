"""Configuración global - Variables de entorno desde .env"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.absolute()
load_dotenv(dotenv_path=ROOT_DIR / '.env')

# Cámara Hikvision
URL = os.getenv('CAMERA_URL')
USERNAME = os.getenv('CAMERA_USERNAME')
PASSWORD = os.getenv('CAMERA_PASSWORD')
INTERVALO_CONSULTA = int(os.getenv('INTERVALO_CONSULTA', 1))

# Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# XML para filtrado de eventos
BODY_XML = """
<AfterTime>
    <picTime>20250415T000000-500</picTime>
</AfterTime>
"""

HEADERS = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

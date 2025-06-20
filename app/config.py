"""
Configuración global del Sistema de Detección de Placas

Carga variables desde .env para seguridad de credenciales.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta del directorio raíz del proyecto (un nivel arriba de app/)
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv(dotenv_path=ROOT_DIR / '.env')

# Configuración de la cámara/API de placas
URL = os.getenv('CAMERA_URL')
USERNAME = os.getenv('CAMERA_USERNAME')
PASSWORD = os.getenv('CAMERA_PASSWORD')
INTERVALO_CONSULTA = int(os.getenv('INTERVALO_CONSULTA', 1))

# Configuración de la API de citas
URL_CITAS = os.getenv('URL_CITAS')
NO_CIA = os.getenv('NO_CIA')
AGENCIA = os.getenv('AGENCIA')

# XML con fecha de inicio para filtrar eventos, no necesario
BODY_XML = """
<AfterTime>
    <picTime>20250415T000000-500</picTime>
</AfterTime>
"""

# Encabezados HTTP para las solicitudes a la API de la cámara
HEADERS = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

"""
Archivo de configuración global del Sistema de Detección de Placas

Este módulo centraliza todas las variables de configuración utilizadas por 
los diferentes componentes del sistema, facilitando su mantenimiento y ajuste.

Los parámetros se organizan en secciones según su función:
- Configuración de la cámara/API de placas
- Configuración de la API de citas
- Configuración de la base de datos MySQL

Las credenciales y datos sensibles se cargan desde un archivo .env
para mayor seguridad y facilidad de configuración.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la cámara/API de placas
# ---------------------------------------
# URL de la API de la cámara Hikvision para detección de placas
URL = os.getenv('CAMERA_URL')
# Credenciales de autenticación para la cámara
USERNAME = os.getenv('CAMERA_USERNAME')
PASSWORD = os.getenv('CAMERA_PASSWORD')
# Intervalo en segundos entre consultas consecutivas a la cámara
INTERVALO_CONSULTA = int(os.getenv('INTERVALO_CONSULTA', 1))

# Configuración de la API de citas
# ---------------------------------------
# URL del servicio web para consultar citas por número de placa
URL_CITAS = os.getenv('URL_CITAS')
# Parámetros de identificación de la compañía y agencia
NO_CIA = os.getenv('NO_CIA')
COD_AGENCIA = os.getenv('COD_AGENCIA')

# XML con la fecha de inicio de búsqueda para filtrar eventos de la cámara
# ---------------------------------------
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

# Configuración de la base de datos MySQL
# ---------------------------------------
# Esta configuración se utiliza solo para diagnóstico, los datos se envían al servidor remoto
DB_CONFIG = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "user": os.getenv('DB_USER', 'root'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE', 'placas')
}
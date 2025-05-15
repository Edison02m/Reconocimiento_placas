# Configuración de la cámara/API de placas
URL = "http://192.168.20.45/ISAPI/Traffic/channels/1/vehicleDetect/plates"
USERNAME = "admin"
PASSWORD = "Telcomexpert01"
INTERVALO_CONSULTA = 1  # segundos entre consultas

# Configuración de la API de citas
URL_CITAS = "https://s3s.suzukiecuador.com/casabacaWebservices/agendamientoCitas/consultaPorPlaca"
NO_CIA = "08"
COD_AGENCIA = "05"

# XML con la fecha de inicio de búsqueda
BODY_XML = """
<AfterTime>
    <picTime>20250415T000000-500</picTime>
</AfterTime>
"""

HEADERS = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin123",  # Actualiza con tu contraseña
    "database": "placas"
} 
"""
Archivo de configuración global del Sistema de Detección de Placas

Este módulo centraliza todas las variables de configuración utilizadas por 
los diferentes componentes del sistema, facilitando su mantenimiento y ajuste.

Los parámetros se organizan en secciones según su función:
- Configuración de la cámara/API de placas
- Configuración de la API de citas
- Configuración de la base de datos MySQL

Nota: En un entorno de producción, es recomendable almacenar credenciales
sensibles utilizando variables de entorno u otros métodos seguros.
"""

# Configuración de la cámara/API de placas
# ---------------------------------------
# URL de la API de la cámara Hikvision para detección de placas
URL = "http://192.168.20.45/ISAPI/Traffic/channels/1/vehicleDetect/plates"
# Credenciales de autenticación para la cámara
USERNAME = "admin"
PASSWORD = "Telcomexpert01"
# Intervalo en segundos entre consultas consecutivas a la cámara
INTERVALO_CONSULTA = 1  

# Configuración de la API de citas
# ---------------------------------------
# URL del servicio web para consultar citas por número de placa
URL_CITAS = "https://s3s.suzukiecuador.com/casabacaWebservices/agendamientoCitas/consultaPorPlaca"
# Parámetros de identificación de la compañía y agencia
NO_CIA = "08"
COD_AGENCIA = "05"

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
    "host": "localhost",
    "user": "root",
    "password": "admin123",  # Para producción, usar variables de entorno
    "database": "placas"
} 
# Sistema de Detección de Placas - Suzuki

Sistema profesional para la detección automática de placas vehiculares y verificación de citas programadas en concesionarios Suzuki.

## Características principales

- **Detección automática**: Captura y reconocimiento de placas vehiculares en tiempo real
- **Verificación de citas**: Integración con la API de agendamiento de Suzuki
- **Salida por consola**: Muestra información clara sobre placas detectadas y estado de citas
- **Registro remoto**: Envía los datos de placas detectadas a un servidor remoto
- **Monitoreo de dispositivos**: Verificación del estado de las cámaras
- **Configuración flexible**: Variables de entorno para personalización fácil

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar su mantenimiento:

```
├── app/
│   ├── __init__.py        # Inicialización del paquete
│   ├── config.py          # Configuración global y variables de entorno
│   ├── camera.py          # Comunicación con la cámara IP
│   ├── api_citas.py       # Integración con la API de citas de Suzuki
│   ├── database.py        # Envío de datos al servidor remoto
│   ├── monitor.py         # Monitoreo continuo de placas
│   └── state.py           # Estado compartido
├── .env                   # Configuración de entorno
└── run.py                 # Punto de entrada principal
```

## Funcionalidades detalladas

### Detección de placas
- Utiliza cámaras Hikvision con capacidad ANPR (Automatic Number Plate Recognition)
- Comunicación vía API REST con formato XML
- Procesamiento de eventos de detección en tiempo real

### Consulta de citas
- Integración con la API de citas de Suzuki
- Verificación en tiempo real de citas programadas
- Estados de respuesta:
  - CITA ENCONTRADA: Cuando el vehículo tiene una cita programada
  - NO SE ENCONTRARON RESULTADOS: Cuando no hay cita registrada
- Validación de formato de placas para asegurar consistencia

### Almacenamiento de datos
- Registro completo de todas las placas detectadas
- Envío automático a servidor remoto mediante peticiones HTTP
- Configuración flexible del servidor remoto mediante variables de entorno

## Hardware compatible

- **Cámaras compatibles**: Cualquier cámara con capacidad de reconocimiento de placas (ANPR)
- **Protocolo**: Comunicación vía HTTP/HTTPS con la API de la cámara
- **Configuración**: Dirección IP fija o nombre de dominio del servidor de cámaras

## Requisitos del sistema

- Python 3.6+
- Dependencias principales:
  - requests
  - python-dotenv
- Conexión a Internet para comunicación con la API de Suzuki
- Acceso al servidor de cámaras en la red local

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Edison02m/Reconocimiento_placas.git
cd Reconocimiento_placas
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
   - Copia el archivo `.env.example` a `.env`
   - Edita el archivo `.env` con la configuración de tu entorno:
     - Configuración de la cámara (URL, usuario, contraseña)
     - URL de la API de citas de Suzuki
     - Código de compañía y agencia
     - URL del servidor remoto para registro de placas

## Uso

Para iniciar el sistema:

```bash
python run.py
```

El sistema mostrará la información de placas detectadas y citas en la consola. Para detener el sistema, presione Ctrl+C.

## Configuración del entorno

El archivo `.env` debe contener las siguientes variables:

```
# Configuración de la cámara/API de placas
CAMERA_URL=http://direccion-ip-camara/ISAPI/Traffic/channels/1/vehicleDetect/plates
CAMERA_USERNAME=usuario
CAMERA_PASSWORD=contraseña
INTERVALO_CONSULTA=1

# Configuración de la API de citas
URL_CITAS=https://s3s.suzukiecuador.com/casabacaWebservices/agendamientoCitas/consultaPorPlaca
NO_CIA=08
COD_AGENCIA=06

# Configuración del servidor remoto
REMOTE_SERVER_URL=http://direccion-ip-servidor
```

## Mejoras implementadas

### 1. Integración con API de Suzuki
- Consulta directa a la API de citas de Suzuki
- Validación de formato de placas
- Manejo de errores mejorado

### 2. Optimización de código
- Eliminación de código innecesario
- Mejor manejo de recursos
- Código más limpio y mantenible

### 3. Despliegue simplificado
- Configuración mediante variables de entorno
- Sin dependencias de bases de datos locales
- Fácil integración con sistemas existentes

## Solución de problemas

- **Error de conexión a la cámara**: Verifica la URL, usuario y contraseña en el archivo `.env`
- **Error al consultar citas**: Asegúrate de que el servidor tenga acceso a Internet y a la API de Suzuki
- **Placas no detectadas**: Verifica la configuración de la cámara y la calidad de la imagen

## Soporte

Para soporte técnico, contacta al equipo de desarrollo.

## Licencia

Este proyecto es de uso interno de Suzuki Ecuador. Todos los derechos reservados.
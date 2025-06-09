# Sistema de Detección de Placas Vehiculares - Suzuki

Sistema profesional para la detección automática de placas vehiculares, verificación de citas programadas y registro remoto en concesionarios Suzuki Ecuador. El sistema integra cámaras ANPR Hikvision, consulta una API de citas y almacena los eventos en un servidor remoto. Todo el flujo es monitoreado y mostrado en consola en tiempo real.

## Características principales

- **Detección automática**: Captura y reconocimiento de placas vehiculares en tiempo real usando cámaras Hikvision ANPR.
- **Limpieza y validación**: Las placas detectadas son limpiadas automáticamente (se eliminan todos los caracteres especiales, solo quedan letras y números) antes de ser procesadas o almacenadas.
- **Verificación de citas**: Integración directa con la API de agendamiento de Suzuki para consultar citas por placa.
- **Registro remoto**: Todas las placas detectadas se envían automáticamente a un servidor remoto PHP/MySQL vía HTTP POST. La base de datos local es solo para diagnóstico.
- **Monitoreo continuo**: Un hilo daemon verifica constantemente nuevas placas y actualiza el estado global del sistema.
- **Salida por consola**: Visualización clara y detallada de cada evento detectado, incluyendo datos de la cita si existe.
- **Configuración flexible**: Variables de entorno (.env) para personalizar URLs, credenciales y parámetros de consulta.

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar su mantenimiento y escalabilidad:

```
├── app/
│   ├── __init__.py        # Inicialización del paquete
│   ├── config.py          # Carga y gestión de variables de entorno (.env)
│   ├── camera.py          # Comunicación con la cámara Hikvision ANPR (detección y limpieza de placas)
│   ├── api_citas.py       # Consulta a la API de citas de Suzuki
│   ├── database.py        # Envío de datos de placas al servidor remoto (PHP/MySQL)
│   ├── monitor.py         # Hilo de monitoreo continuo y procesamiento de eventos
│   └── state.py           # Estado global de la aplicación y control de duplicados
├── .env                   # Variables de entorno (no se sube al repo)
├── requirements.txt       # Dependencias de Python
├── run.py                 # Punto de entrada principal del sistema
├── database_setup.sql     # Script ejemplo de base diagnóstica local (opcional)
```

## Flujo de funcionamiento principal

1. **Inicialización**: El sistema verifica la conexión con la cámara y el servidor remoto.
2. **Monitoreo**: Un hilo en segundo plano consulta periódicamente la cámara por nuevas placas detectadas.
3. **Limpieza de placas**: Cada placa es limpiada con una expresión regular para eliminar caracteres especiales (solo quedan letras y números).
4. **Almacenamiento**: La placa y la fecha/hora de detección se envían al servidor remoto vía HTTP POST.
5. **Consulta de cita**: Se consulta la API de Suzuki para verificar si la placa tiene cita programada.
6. **Visualización**: Toda la información se muestra en consola en tiempo real, incluyendo detalles de la cita si existe.

## Funcionalidades detalladas

### Detección y limpieza de placas
- Uso de cámaras Hikvision ANPR (API REST/XML)
- Limpieza automática de placas detectadas (`re.sub(r'[^A-Za-z0-9]', '', plate_number)`) para asegurar consistencia
- Procesamiento de eventos en tiempo real

### Consulta de citas
- Integración directa con la API REST de Suzuki
- Consulta y visualización de citas por placa
- Manejo robusto de errores y mensajes claros en consola

### Almacenamiento y diagnóstico
- Registro automático de todas las placas detectadas en un servidor remoto
- Diagnóstico y pruebas de conexión disponibles desde consola
- Base de datos local solo para pruebas/diagnóstico

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

1. Clona el repositorio o copia los archivos al servidor:

```bash
git clone https://github.com/Edison02m/Reconocimiento_placas.git
cd Reconocimiento_placas
```

2. Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
   - Crea un archivo `.env` en la raíz del proyecto (puedes copiar y renombrar `.env.example` si existe).
   - Edita el archivo `.env` con la configuración de tu entorno:
     - URL y credenciales de la cámara Hikvision
     - URL de la API de citas de Suzuki
     - Código de compañía y agencia
     - URL del servidor remoto para registro de placas

## Uso

Para iniciar el sistema, ejecuta:

```bash
python run.py
```

El sistema mostrará en consola cada placa detectada, la fecha/hora, el estado de la cita (si existe), y los datos principales de la cita. Para detener el sistema, presiona Ctrl+C.

## Configuración del entorno

El archivo `.env` debe contener las siguientes variables (ajusta según tu entorno):

```
# Configuración de la cámara Hikvision
CAMERA_URL=http://direccion-ip-camara/ISAPI/Traffic/channels/1/vehicleDetect/plates
CAMERA_USERNAME=usuario
CAMERA_PASSWORD=contraseña
INTERVALO_CONSULTA=1

# Configuración de la API de citas Suzuki
URL_CITAS=https://s3s.suzukiecuador.com/casabacaWebservices/agendamientoCitas/consultaPorPlaca
NO_CIA=08
COD_AGENCIA=06

# Configuración del servidor remoto para registro de placas
REMOTE_SERVER_URL=http://direccion-ip-servidor
```

## Mejoras y detalles técnicos relevantes

- Limpieza de placas: Antes de guardar o consultar una placa, se eliminan todos los caracteres especiales (solo letras y números) para evitar errores y asegurar consistencia (ver función `get_plates()` en `camera.py`).
- El almacenamiento principal es remoto (servidor PHP/MySQL), la base de datos local es solo diagnóstica.
- El sistema es tolerante a fallos: errores de conexión o API no detienen el monitoreo.
- El monitoreo y procesamiento es completamente asíncrono y en tiempo real.
- Toda la configuración sensible se realiza vía variables de entorno.

## Solución de problemas

- **Error de conexión a la cámara**: Verifica la URL, usuario y contraseña en el archivo `.env` y la conectividad de red.
- **Error al consultar citas**: Asegúrate de que el servidor tenga acceso a Internet y la URL de la API esté correctamente configurada.
- **Placas no detectadas**: Revisa la configuración de la cámara, la calidad de la imagen y que la cámara tenga capacidad ANPR.
- **Datos no almacenados**: Verifica la URL del servidor remoto y la conectividad.

## Soporte y contribución

Para soporte técnico, contacta al equipo de desarrollo.

Si deseas contribuir, abre un issue o pull request en el repositorio oficial.

## Licencia

Este proyecto es de uso interno de Suzuki Ecuador. Todos los derechos reservados.
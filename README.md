# Sistema de Detección de Placas - Casabaca

Este sistema permite detectar automáticamente las placas de los vehículos que ingresan a las instalaciones de Casabaca y verificar si tienen citas programadas.

## Estructura del Proyecto

El proyecto ha sido refactorizado en una estructura modular para facilitar su mantenimiento:

```
├── app/
│   ├── __init__.py        # Inicialización de la aplicación Flask
│   ├── config.py          # Configuración global
│   ├── camera.py          # Comunicación con la cámara IP
│   ├── api_citas.py       # Consulta a API de citas
│   ├── database.py        # Conexión y operaciones con la base de datos
│   ├── monitor.py         # Monitoreo continuo de placas
│   ├── routes.py          # Rutas web
│   ├── state.py           # Estado compartido
│   ├── templates.py       # Gestión de plantillas HTML
│   └── templates/
│       ├── index.html     # Interfaz web principal
│       └── admin.html     # Interfaz de administración
└── run.py                 # Punto de entrada
```

## Características

- **Detección de placas**: Captura automática de placas vehiculares usando cámaras Hikvision
- **Consulta de citas**: Verifica si los vehículos detectados tienen citas programadas
- **Almacenamiento en base de datos**: Registro histórico de todas las placas detectadas
- **Panel de administración**: Gestión de dispositivos y visualización del historial de detecciones

## Hardware Compatible

- **Modelo de cámara recomendado**: IDS-2CD7A46G0/P-IZHSY
- Cámaras Hikvision con capacidad de reconocimiento de placas (ANPR)
- Comunicación vía TCP/IP con direccionamiento fijo de IP

## Requisitos

- Python 3.6+
- Flask
- requests
- mysql-connector-python

## Instalación

1. Clona el repositorio:

```bash
git clone [url-del-repositorio]
cd [nombre-del-directorio]
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura la base de datos MySQL:
   - Crea una base de datos llamada `placas`
   - Ejecuta el script SQL para crear la tabla `registro_placas`
   - Actualiza la configuración en `app/config.py` si es necesario

## Uso

Para iniciar el sistema:

```bash
python run.py
```

La interfaz web estará disponible en:
- **Monitor principal**: `http://localhost:5000`
- **Panel de administración**: `http://localhost:5000/admin`

## Configuración

Edita el archivo `app/config.py` para ajustar:

- URL de la cámara IP
- Credenciales de acceso
- Configuración de la base de datos
- URL del servicio de citas

## Desarrollado por

Casabaca - Departamento de Tecnología 
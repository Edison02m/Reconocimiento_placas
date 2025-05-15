# Sistema de Detección de Placas - Casabaca

Sistema profesional para la detección automática de placas vehiculares y verificación de citas programadas en concesionarios Toyota Casabaca.

## Características principales

- **Detección automática**: Captura y reconocimiento de placas vehiculares en tiempo real
- **Verificación de citas**: Consulta inmediata al sistema de agendamiento de Casabaca
- **Interfaz visual mejorada**: Muestra claramente el estado de cita con colores e iconos intuitivos
- **Historial completo**: Registro y consulta del historial de placas detectadas con paginación
- **Monitoreo de dispositivos**: Panel de administración para verificar el estado de las cámaras
- **Arquitectura modular**: Diseño refactorizado para facilitar mantenimiento y extensibilidad

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
├── database_setup.sql     # Script para configuración inicial de la BD
└── run.py                 # Punto de entrada
```

## Funcionalidades detalladas

### Detección de placas
- Utiliza cámaras Hikvision con capacidad ANPR (Automatic Number Plate Recognition)
- Comunicación vía API REST con formato XML
- Procesamiento de eventos de detección en tiempo real

### Consulta de citas
- Integración con el servicio web de citas de Casabaca
- Presentación clara de estados de cita:
  - CITA CONFIRMADA (verde): Cuando el vehículo tiene una cita programada
  - NO TIENE CITA / NO SE ENCONTRARON RESULTADOS (rojo): Cuando no hay cita
- Visualización de información detallada del cliente y vehículo

### Almacenamiento de datos
- Registro completo de todas las placas detectadas
- Doble almacenamiento: servidor remoto principal y base de datos local de respaldo
- Capacidad de filtrado y paginación para grandes volúmenes de datos

### Interfaz de usuario
- Diseño moderno y responsivo usando Bootstrap 5
- Identidad visual de Casabaca Toyota
- Interfaz principal para visualizar la última detección
- Panel de administración para monitoreo y consulta del historial

## Hardware compatible

- **Modelo de cámara recomendado**: Hikvision IDS-2CD7A46G0/P-IZHSY
- Cualquier cámara Hikvision con capacidad de reconocimiento de placas (ANPR)
- Comunicación vía TCP/IP con direccionamiento fijo de IP

## Requisitos del sistema

- Python 3.6+
- Flask
- Requests
- MySQL-connector-python
- Conexión a red TCP/IP para comunicación con la cámara
- Servidor MySQL para almacenamiento (opcional para diagnóstico)

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

3. Configura la base de datos MySQL (opcional para diagnóstico):
   - Crea una base de datos llamada `placas`
   - Ejecuta el script SQL para crear la tabla `registro_placas`:
   ```bash
   mysql -u root -p placas < database_setup.sql
   ```
   - Actualiza la configuración en `app/config.py` si es necesario

4. Configura las direcciones IP y credenciales:
   - Edita `app/config.py` con la información de tu cámara y servidor

## Uso

Para iniciar el sistema:

```bash
python run.py
```

La interfaz web estará disponible en:
- **Monitor principal**: `http://localhost:5000`
- **Panel de administración**: `http://localhost:5000/admin`

## Mejoras implementadas

### 1. Refactorización modular
- División del código monolítico en módulos especializados
- Mayor facilidad de mantenimiento y extensibilidad
- Separación clara de responsabilidades

### 2. Paginación y búsqueda de registros
- Implementación de paginación en el historial de placas
- Filtrado por número de placa
- Mejor rendimiento con grandes volúmenes de datos

### 3. Mejora en la visualización de citas
- Rediseño de la interfaz para mostrar claramente el estado de cita
- Presentación destacada de la información importante
- Mensaje claro cuando no se encuentran resultados

### 4. Documentación completa
- Docstrings detallados explicando cada módulo y función
- Comentarios explicativos en el código
- README con instrucciones claras para instalación y uso

## Desarrollado por

Departamento de Tecnología - Casabaca Toyota Ecuador 
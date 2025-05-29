# Sistema de Detección de Placas - Casabaca

Sistema profesional para la detección automática de placas vehiculares y verificación de citas programadas en concesionarios Toyota Casabaca.

## Características principales

- **Detección automática**: Captura y reconocimiento de placas vehiculares en tiempo real
- **Verificación de citas**: Consulta inmediata al sistema de agendamiento de Casabaca
- **Salida por consola**: Muestra información clara sobre placas detectadas y estado de citas
- **Historial completo**: Registro del historial de placas detectadas en servidor remoto
- **Monitoreo de dispositivos**: Verificación del estado de las cámaras
- **Arquitectura modular**: Diseño refactorizado para facilitar mantenimiento y extensibilidad

## Estructura del Proyecto

El proyecto ha sido refactorizado en una estructura modular para facilitar su mantenimiento:

```
├── app/
│   ├── __init__.py        # Inicialización del paquete
│   ├── config.py          # Configuración global
│   ├── camera.py          # Comunicación con la cámara IP
│   ├── api_citas.py       # Consulta a API de citas
│   ├── database.py        # Conexión y operaciones con la base de datos
│   ├── monitor.py         # Monitoreo continuo de placas
│   └── state.py           # Estado compartido
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
  - CITA ENCONTRADA: Cuando el vehículo tiene una cita programada
  - NO SE ENCONTRARON RESULTADOS: Cuando no hay cita
- Visualización de información detallada del cliente y vehículo en consola

### Almacenamiento de datos
- Registro completo de todas las placas detectadas
- Almacenamiento en servidor remoto con respaldo opcional en base de datos local

## Hardware compatible

- **Modelo de cámara recomendado**: Hikvision IDS-2CD7A46G0/P-IZHSY
- Cualquier cámara Hikvision con capacidad de reconocimiento de placas (ANPR)
- Comunicación vía TCP/IP con direccionamiento fijo de IP

## Requisitos del sistema

- Python 3.6+
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

El sistema mostrará la información de placas detectadas y citas en la consola. Para detener el sistema, presione Ctrl+C.

## Mejoras implementadas

### 1. Refactorización modular
- División del código monolítico en módulos especializados
- Mayor facilidad de mantenimiento y extensibilidad
- Separación clara de responsabilidades

### 2. Optimización para funcionamiento en consola
- Eliminación de la interfaz web para un funcionamiento más ligero
- Salida clara y estructurada en consola
- Mejor rendimiento en sistemas con recursos limitados

### 3. Mejora en la visualización de citas
- Presentación destacada de la información importante
- Mensaje claro cuando no se encuentran resultados

### 4. Documentación completa
- Docstrings detallados explicando cada módulo y función
- Comentarios explicativos en el código
- README con instrucciones claras para instalación y uso

## Desarrollado por

Departamento de Tecnología - Casabaca Toyota Ecuador 
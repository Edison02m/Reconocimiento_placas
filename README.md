# Sistema de Detección de Placas Vehiculares - Suzuki

Sistema para la detección automática de placas vehiculares y verificación de citas programadas en concesionarios Suzuki Ecuador. El sistema integra cámaras ANPR Hikvision y consulta una API de citas. Todo el flujo es monitoreado y mostrado en consola en tiempo real.

## Características principales

- **Detección automática**: Captura y reconocimiento de placas vehiculares en tiempo real usando cámaras Hikvision ANPR.
- **Limpieza y validación**: Las placas detectadas son limpiadas automáticamente (se eliminan todos los caracteres especiales, solo quedan letras y números) antes de ser procesadas o almacenadas.
- **Verificación de citas**: Integración directa con la API de Suzuki para consultar citas por placa.
- **Monitoreo en tiempo real**: Visualización de placas detectadas y verificación de citas directamente en consola.
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
│   ├── monitor.py         # Hilo de monitoreo continuo y procesamiento de eventos
│   └── state.py           # Estado global de la aplicación y control de duplicados
├── .env                   # Variables de entorno (no se sube al repo)
├── requirements.txt       # Dependencias de Python
├── run.py                 # Punto de entrada principal del sistema
```

## Flujo de funcionamiento principal

1. **Inicialización**: El sistema verifica la conexión con la cámara.
2. **Monitoreo**: Un hilo en segundo plano consulta periódicamente la cámara por nuevas placas detectadas.
3. **Limpieza de placas**: Cada placa es limpiada con una expresión regular para eliminar caracteres especiales (solo quedan letras y números).
4. **Consulta de cita**: Se consulta la API de Suzuki para verificar si la placa tiene cita programada.
5. **Visualización**: Toda la información se muestra en consola en tiempo real, incluyendo detalles de la cita si existe.

## Requisitos del sistema

- Python 3.6+
- Dependencias principales:
  - requests
  - python-dotenv
- Conexión a Internet para comunicación con la API de Suzuki
- Acceso al servidor de cámaras en la red local

## Instalación

1. Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

## Uso

Para iniciar el sistema, ejecuta:

```bash
python run.py
```

El sistema mostrará en consola cada placa detectada, la fecha/hora, el estado de la cita (si existe), y los datos principales de la cita. Para detener el sistema, presiona Ctrl+C.

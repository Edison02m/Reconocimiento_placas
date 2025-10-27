# Sistema de Detección de Placas Vehiculares - Suzuki

Sistema de detección automática de placas vehiculares con cámaras ANPR Hikvision y almacenamiento en Supabase.

## Características

- **Detección automática** de placas en tiempo real con cámaras Hikvision ANPR
- **Limpieza de placas** (solo letras y números, sin caracteres especiales)
- **Almacenamiento optimizado** en Supabase (~70-80% más rápido con HTTP pooling)
- **Monitoreo continuo** cada 1 segundo con control de duplicados
- **Visualización en consola** de cada detección en tiempo real
- **Configuración flexible** con variables de entorno (.env)

## Estructura del Proyecto

```
├── app/
│   ├── camera.py          # Comunicación con cámara Hikvision (XML + HTTP Digest)
│   ├── config.py          # Variables de entorno
│   ├── monitor.py         # Monitoreo continuo y procesamiento
│   ├── state.py           # Estado global de la aplicación
│   └── supabase_client.py # Cliente Supabase optimizado
├── .env                   # Variables de entorno (no incluido en repo)
├── requirements.txt       # Dependencias Python
├── run.py                 # Punto de entrada principal
└── iniciar_sistema.bat    # Script de inicio rápido (Windows)
```

## Flujo de Funcionamiento

1. **Inicialización**: Verifica conexión con cámara y Supabase
2. **Monitoreo**: Consulta cada 1 segundo por nuevas placas
3. **Limpieza**: Elimina caracteres especiales de la placa
4. **Validación**: Control de duplicados (placa + fecha exacta)
5. **Envío**: Almacenamiento optimizado en Supabase
6. **Visualización**: Muestra detección en consola

## Requisitos

- Python 3.6+
- Dependencias: `requests`, `python-dotenv`, `supabase`, `httpx`
- Conexión a Internet (Supabase)
- Acceso a cámara Hikvision en red local

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

**Opción 1 - Script batch (Windows):**
```bash
iniciar_sistema.bat
```

**Opción 2 - Python directo:**
```bash
python run.py
```

Para detener: `Ctrl+C`

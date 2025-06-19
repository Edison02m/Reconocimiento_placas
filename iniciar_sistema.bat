@echo off
echo Iniciando Sistema de Deteccion de Placas...
cd /d "c:\Users\Edison\Desktop\placas\Reconocimiento_placas"
echo Directorio actual: %CD%
echo Verificando archivo .env...
if exist ".env" (
    echo Archivo .env encontrado
) else (
    echo ERROR: Archivo .env NO encontrado
)
echo Ejecutando Python...
python -c "import os; print('Python ejecutandose desde:', os.getcwd())"
python run.py
echo.
echo Presiona cualquier tecla para cerrar...
pause

## Posibles Causas del Problema

### 1. **Variables de Entorno del Sistema**
Cuando ejecutas desde consola, heredas todas las variables de entorno de tu sesión actual. El `.bat` puede no tener acceso a las mismas variables.

### 2. **Codificación de Caracteres**
El archivo `.env` o el `.bat` pueden tener problemas de codificación. Verifica que ambos estén guardados en UTF-8.

### 3. **Permisos de Ejecución**
El `.bat` puede no tener los mismos permisos que cuando ejecutas directamente en consola.

## Soluciones a Probar

### Solución 1: Modificar el .bat con más diagnósticos
```batch
@echo off
echo Iniciando Sistema de Deteccion de Placas...
cd /d "c:\Users\Edison\Desktop\placas\Reconocimiento_placas"
echo Directorio actual: %CD%
echo Verificando archivo .env...
if exist ".env" (
    echo Archivo .env encontrado
) else (
    echo ERROR: Archivo .env NO encontrado
)
echo Ejecutando Python...
python -c "import os; print('Python ejecutandose desde:', os.getcwd())"
python run.py
echo.
echo Presiona cualquier tecla para cerrar...
pause
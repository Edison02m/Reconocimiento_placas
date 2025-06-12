@echo off
echo Iniciando Sistema de Deteccion de Placas...
cd /d "c:\Users\Edison\Desktop\placas\Reconocimiento_placas"
python run.py
pause

## Opción 2: Redirigir la salida a un archivo de registro (log)

Otra opción es modificar el archivo batch para que guarde todos los mensajes en un archivo de texto que puedas revisar después:
```batch
@echo off
echo Iniciando Sistema de Deteccion de Placas... > "%~dp0logs.txt"
cd /d "c:\Users\Edison\Desktop\placas\Reconocimiento_placas"
python run.py >> "%~dp0logs.txt" 2>&1
```
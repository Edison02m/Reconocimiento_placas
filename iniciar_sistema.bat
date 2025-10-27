@echo off
echo ========================================
echo   Sistema de Deteccion de Placas
echo ========================================
echo.

cd /d "c:\Users\Edison\Desktop\Reconocimiento_Placas\Reconocimiento_placas"

echo [1/4] Verificando directorio...
echo Directorio: %CD%
echo.

echo [2/4] Instalando/Actualizando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo X ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas correctamente
echo.

echo [3/4] Verificando archivo .env...
if exist ".env" (
    echo ✓ Archivo .env encontrado
) else (
    echo X ERROR: Archivo .env NO encontrado
    pause
    exit /b 1
)
echo.

echo [4/4] Iniciando sistema...
python run.py

echo.
echo ========================================
pause
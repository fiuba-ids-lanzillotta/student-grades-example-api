@echo off
setlocal enabledelayedexpansion

echo === Configuracion del ambiente con virtualenv ===

REM Verificar que Python esta instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, descargalo desde https://www.python.org/downloads/
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [OK] %%v instalado

REM Verificar que pip esta disponible
python -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: pip no esta disponible. Reinstala Python habilitando la opcion "pip".
    exit /b 1
)
echo [OK] pip disponible

REM Verificar e instalar virtualenv si es necesario
python -m virtualenv --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo virtualenv no esta instalado. Instalando...
    python -m pip install --no-warn-script-location virtualenv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo instalar virtualenv.
        exit /b 1
    )
    echo [OK] virtualenv instalado
) else (
    echo [OK] virtualenv ya esta instalado
)

REM Crear el ambiente virtual
echo Creando ambiente virtual...
if not exist ".venv" (
    python -m virtualenv .venv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo crear el ambiente virtual.
        exit /b 1
    )
    echo [OK] Ambiente virtual creado
) else (
    echo [OK] El ambiente virtual ya existe
)

REM Activar el ambiente virtual
echo Activando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar que el ambiente virtual esta activo
if "%VIRTUAL_ENV%"=="" (
    echo ERROR: No se pudo activar el ambiente virtual.
    exit /b 1
)
echo [OK] Ambiente virtual activado: %VIRTUAL_ENV%

REM Instalar dependencias
echo Instalando dependencias desde requirements.txt...
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias.
    exit /b 1
)

REM Mostrar informacion final
echo.
echo === [OK] Configuracion completada ===
echo Para activar el ambiente virtual en futuras sesiones, ejecuta:
echo   .venv\Scripts\activate
echo.
echo Para desactivar el ambiente virtual, ejecuta:
echo   deactivate
echo.
echo Asegurate de tener la base de datos MySQL corriendo:
echo   docker compose up -d
echo.
echo Iniciando la aplicacion...
echo.

REM Levantar la aplicacion
python app.py

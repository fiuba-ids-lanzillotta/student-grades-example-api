@echo off
setlocal enabledelayedexpansion

echo === Configuracion del ambiente con pipenv ===

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

REM Verificar e instalar pipx si es necesario
python -m pipx --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pipx no esta instalado. Instalando...
    python -m pip install --user --no-warn-script-location pipx
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo instalar pipx.
        exit /b 1
    )
    echo [OK] pipx instalado
) else (
    echo [OK] pipx ya esta instalado
)

REM Verificar e instalar pipenv si es necesario
python -m pipx run pipenv --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pipenv no esta instalado. Instalando con pipx...
    python -m pipx install pipenv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo instalar pipenv.
        exit /b 1
    )
    echo [OK] pipenv instalado
) else (
    for /f "tokens=*" %%v in ('python -m pipx run pipenv --version 2^>^&1') do echo [OK] %%v instalado
)

REM Crear el Pipfile desde requirements.txt si no existe
if not exist "Pipfile" (
    echo Creando Pipfile e instalando dependencias...
    python -m pipx run pipenv install --requirements requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo crear el ambiente con pipenv.
        exit /b 1
    )
    echo [OK] Pipfile creado e instaladas dependencias
) else (
    echo [OK] El Pipfile ya existe
    echo Instalando dependencias con pipenv...
    python -m pipx run pipenv install
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias.
        exit /b 1
    )
)

echo.
echo === [OK] Configuracion completada ===
echo Para activar el ambiente virtual en futuras sesiones, ejecuta:
echo   python -m pipx run pipenv shell
echo.
echo Para desactivar el ambiente virtual, ejecuta:
echo   exit
echo.
echo Asegurate de tener la base de datos MySQL corriendo:
echo   docker compose up -d
echo.
echo Iniciando la aplicacion...
echo.

python -m pipx run pipenv run python app.py

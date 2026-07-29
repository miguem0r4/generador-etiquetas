@echo off
title Generador de Etiquetas
chcp 65001 >nul

:: Intentar con py (launcher) o python
set PYTHON=
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=py
) else (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON=python
    ) else (
        echo [ERROR] No se encontro Python.
        echo.
        echo Instala Python desde https://www.python.org/downloads/
        echo IMPORTANTE: marca la casilla "Add Python to PATH" durante la instalacion.
        echo.
        pause
        exit /b 1
    )
)

echo [1/4] Actualizando pip ...
%PYTHON% -m pip install --upgrade pip >nul 2>&1

echo [2/4] Instalando dependencias ...
%PYTHON% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Fallo la instalacion de dependencias.
    pause
    exit /b 1
)

echo [3/4] Verificando dependencias ...
%PYTHON% -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo importar customtkinter. Revisa la instalacion.
    pause
    exit /b 1
)

echo [4/4] Iniciando aplicacion ...
echo.
%PYTHON% main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La aplicacion se cerro con un error.
    pause
    exit /b 1
)

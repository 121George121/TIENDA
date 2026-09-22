@echo off
chcp 65001 > nul
title Restaurador de Base de Datos - Shopyn Golden Store
cls
echo ==========================================================
echo   🛍️  SHOPYN GOLDEN STORE - RESTAURADOR DE BASE DE DATOS
echo ==========================================================
echo Iniciando restauración automática de tablas, usuarios, prendas y stock...
echo.

if exist "..\venv\Scripts\python.exe" (
    ..\venv\Scripts\python.exe restaurar_base_datos.py
) else if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe database\restaurar_base_datos.py
) else (
    python restaurar_base_datos.py
)

echo.
echo Presiona cualquier tecla para salir...
pause > nul

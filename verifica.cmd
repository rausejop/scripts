@echo off
setlocal
chcp 65001 > nul

:: ============================================================================
:: Nombre del Script: verifica.cmd
:: Descripción: Descarga un archivo ejecutable con wget y verifica su hash.
:: Autor: Rafael Ausejo Prieto + soporte de Google Gemini Flash 2.5
:: Fecha de creación: 11 de agosto de 2025
::
:: Parámetros de Entrada (definidos en el script):
::   - url: URL de descarga del archivo.
::   - hash_oficial: Hash SHA256 esperado.
::   - nombre_archivo: Nombre del archivo descargado.
::
:: Salida:
::   - Un archivo de log llamado 'descarga_log.txt' con un registro de cada paso.
::   - Mensajes en la consola que informan del progreso y el resultado.
:: ============================================================================

:: ----------------------------------------------------------------------------
:: Variables de configuración
:: ----------------------------------------------------------------------------
set "url=https://www.7-zip.org/a/7z2501-x64.exe"
set "hash_oficial=78afa2a1c773caf3cf7edf62f857d2a8a5da55fb0fff5da416074c0d28b2b55f"
set "nombre_archivo=7z2501-x64.exe"
set "log_file=descarga_log.txt"

:: ----------------------------------------------------------------------------
:: Lógica principal del script
:: ----------------------------------------------------------------------------
call :LogMessage "✅ Iniciando script: verifica.cmd"
call :LogMessage "✅ Autor: Rafael Ausejo Prieto + soporte de Google Gemini Flash 2.5"
call :LogMessage "✅ Este script descargará el fichero: %nombre_archivo%"
call :LogMessage "✅ desde la URL: %url%"
call :LogMessage "✅ Su integridad será verificada con el hash SHA256."

:: Borra el archivo de log anterior si existe
if exist "%log_file%" del "%log_file%"

:: Paso 1: Verificación de wget y descarga del archivo
call :LogMessage "✅ Comprobando la disponibilidad de wget..."
set "wget_cmd="
if exist "%~dp0wget.exe" (
    set "wget_cmd=%~dp0wget.exe"
) else (
    where wget >nul 2>nul
    if %errorlevel% equ 0 (
        set "wget_cmd=wget"
    )
)

if "%wget_cmd%"=="" (
    call :LogMessage "❌ ERROR: El comando 'wget' no se encontró. Asegúrate de que está en el directorio del script o en el PATH."
    goto :fin
)

call :LogMessage "✅ Iniciando la descarga de %url%..."
"%wget_cmd%" --no-check-certificate -O "%nombre_archivo%" "%url%"

:: Verificación de errores en la descarga
if %errorlevel% neq 0 (
    call :LogMessage "❌ ERROR: Fallo al descargar el archivo. Código de salida: %errorlevel%."
    goto :fin
)

:: Verificación adicional: Comprueba si el archivo existe
if not exist "%nombre_archivo%" (
    call :LogMessage "❌ ERROR: La descarga finalizó, pero el archivo '%nombre_archivo%' no se encontró."
    goto :fin
)

call :LogMessage "✅ Descarga completada."

:: Paso 2: Cálculo y verificación del hash
call :LogMessage "✅ Iniciando la verificación del hash SHA256..."
set "hash_descargado="

for /f "skip=1 tokens=*" %%i in ('certutil -hashfile "%nombre_archivo%" SHA256') do (
    set "hash_descargado=%%i"
    goto :comparar_hashes
)

:comparar_hashes
if "%hash_descargado%"=="" (
    call :LogMessage "❌ ERROR: No se pudo calcular el hash del archivo."
    goto :fin
)

if /i "%hash_descargado%"=="%hash_oficial%" (
    call :LogMessage "✅ Éxito: El hash coincide. La integridad del archivo es correcta."
    call :LogMessage "✅ Hash verificado: %hash_descargado%"
) else (
    call :LogMessage "❌ ERROR: El hash NO coincide. El archivo podría estar corrupto o alterado."
    call :LogMessage "❌ Hash oficial:    %hash_oficial%"
    call :LogMessage "❌ Hash calculado: %hash_descargado%"
)

:fin
call :LogMessage "✅ Script finalizado."
endlocal

:: ----------------------------------------------------------------------------
:: FUNCIONES DEL SCRIPT
:: ----------------------------------------------------------------------------
:: La funcion de Log se ha movido al final del script para evitar que termine antes de tiempo.
:: ----------------------------------------------------------------------------
:LogMessage
    echo [%date% %time%] %1
    echo [%date% %time%] %1>> descarga_log.txt
    goto :eof
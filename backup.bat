@echo off
cd /d "%~dp0"
echo ==================================================
echo   INICIANDO RESPALDO MINECRAFT SERVER
echo   Fecha/Hora: %date% %time%
echo ==================================================

python backup.py
if %ERRORLEVEL% equ 0 (
    echo [OK] Respaldo de Minecraft completado exitosamente.
) else (
    echo [ERROR] El respaldo de Minecraft fallo con codigo %ERRORLEVEL%.
)

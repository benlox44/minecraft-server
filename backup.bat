@echo off
cd /d "%~dp0"
echo ==================================================
echo   MINECRAFT SERVER BACKUP STARTED
echo   Date/Time: %date% %time%
echo ==================================================

python backup.py
if %ERRORLEVEL% equ 0 (
    echo [OK] Minecraft backup completed successfully.
) else (
    echo [ERROR] Minecraft backup failed with exit code %ERRORLEVEL%.
)

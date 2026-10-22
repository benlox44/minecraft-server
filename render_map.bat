@echo off
echo Starting Squaremap fullrender at %date% %time% >> "%~dp0squaremap_render.log"
docker exec minecraft rcon-cli "squaremap fullrender overworld" >> "%~dp0squaremap_render.log" 2>&1
echo Finished at %date% %time% >> "%~dp0squaremap_render.log"

set windows-shell := ["cmd.exe", "/c"]

dc := "docker compose"

# Show available commands
default:
    @just --list

# Show available commands
help:
    @just --list

# Start Minecraft server and companion services in background
up:
    {{ dc }} up -d --build

# Stop and remove Minecraft server container
down:
    {{ dc }} down

# Restart Minecraft server
restart:
    {{ dc }} restart

# Stop Minecraft server safely (keeps container)
stop:
    {{ dc }} stop

# Start Minecraft server if stopped
start:
    {{ dc }} start

# Show container status
status:
    {{ dc }} ps

# Follow server logs in real time
logs:
    {{ dc }} logs -f --tail 100

# Open interactive Minecraft RCON console
cli:
    {{ dc }} exec -it minecraft rcon-cli

# Pull latest server image
pull:
    {{ dc }} pull

# Run dedicated Minecraft world backup
backup:
    @python backup.py

# Render squaremap manually in background
render-map:
    @cmd /c render_map.bat

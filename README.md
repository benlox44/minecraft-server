# Minecraft Server Stack

A dedicated Minecraft 26.3 (Fabric) server and companion microservices orchestrated with Docker Compose and Just.

## 📦 Services

| Service | Description | Ports |
| :--- | :--- | :--- |
| **Minecraft** | Fabric dedicated server & Squaremap map viewer | `25565` (Game), `24454/udp` (Voice Chat), `8100` (Squaremap Web UI) |
| **AudioPlayer** | Custom web uploader for in-game audio & music discs | `5000` |

---

## 🚀 Getting Started

### 1. Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose
- [Just](https://github.com/casey/just) command runner
- [Python 3](https://www.python.org/) (for backup automation)

### 2. Environment Configuration
Copy the sample environment file and configure paths as needed:
```bash
copy .env.example .env
```

### 3. Mods Synchronization
Mods for this server are managed through packwiz in the [`minecraft-smp-mods`](https://github.com/benlox44/minecraft-smp-mods) repository. To download or update server mods:
```bash
python path/to/minecraft-smp-mods/download_server_mods.py --dest ./data/mods
```

### 4. Start Server Stack
```bash
just up
```

---

## 🛠️ Management Commands (`justfile`)

All common operations are automated through `just`:

| Recipe | Description |
| :--- | :--- |
| `just up` | Build companion services and start stack in background |
| `just down` | Stop and remove server containers |
| `just restart` | Restart the Minecraft server container |
| `just stop` | Stop server container gracefully |
| `just start` | Start stopped server container |
| `just status` | View container status (`docker compose ps`) |
| `just logs` | Follow live container logs |
| `just cli` | Open interactive Minecraft RCON console |
| `just pull` | Pull latest server images |
| `just backup` | Trigger automated backup to `BACKUP_DIR` |
| `just render-map` | Render squaremap overworld tiles in background |

---

## 💾 Backup Automation

World and configuration backups are automated via `backup.py` / `backup.bat` (`just backup`):
- Flushes live world data to disk via RCON (`save-all flush`).
- Copies server configuration, world data, and audioplayer uploads to `BACKUP_DIR` (e.g., `S:\minecraft-backup`) using optimized `robocopy` mirroring.
- Excludes heavy transient data: rendered map tiles (`squaremap/`), server logs, and compiler caches.
- Retains the 2 most recent full backup snapshots automatically.

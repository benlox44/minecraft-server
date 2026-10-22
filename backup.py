#!/usr/bin/env python3
from __future__ import annotations

import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
BACKUP_RETENTION = 2


def load_env(env_file: Path) -> dict[str, str]:
    env = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, _, v = s.partition("=")
            env[k.strip()] = v.strip().strip("'\"")
    return env


def is_backup_dir(name: str) -> bool:
    if name.startswith("minecraft_"):
        return True
    if len(name) == 17 and "_" in name:
        try:
            datetime.datetime.strptime(name, "%Y-%m-%d_%H%M%S")
            return True
        except ValueError:
            pass
    return False


def main():
    print("=== Minecraft Server Backup Started ===")
    env = load_env(ENV_FILE)
    backup_dest = env.get("BACKUP_DIR", r"S:\minecraft-backup")
    dest_root = Path(backup_dest)
    dest_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    target_dir = dest_root / timestamp

    # 1. Flush world data if server is running
    print("[*] Flushing Minecraft save data to disk...")
    try:
        subprocess.run(["docker", "exec", "minecraft", "rcon-cli", "save-all", "flush"], check=False)
    except Exception:
        pass

    # 2. Sync data folder using robocopy for fast copy
    print(f"[*] Copying data to {target_dir}...")
    source = ROOT / "data"

    args = [
        "robocopy",
        str(source),
        str(target_dir / "data"),
        "/MIR",
        "/FFT",
        "/Z",
        "/XA:H",
        "/W:1",
        "/R:1",
        "/SL",
        "/XD",
        ".git",
        "logs",
        "cache",
        ".cache",
        "crash-reports",
        "squaremap",
    ]
    res = subprocess.run(args)
    if res.returncode >= 8:
        print(f"[ERROR] Robocopy failed with exit code {res.returncode}")
        sys.exit(1)

    # Also copy docker-compose.yml and .env
    shutil.copy2(ROOT / "docker-compose.yml", target_dir / "docker-compose.yml")
    if ENV_FILE.exists():
        shutil.copy2(ENV_FILE, target_dir / ".env")

    # Copy companion service audioplayer code
    audioplayer_src = ROOT / "audioplayer"
    if audioplayer_src.exists():
        shutil.copytree(
            audioplayer_src,
            target_dir / "audioplayer",
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    # 3. Cleanup old backups
    print("[*] Cleaning up old backups...")
    all_backups = sorted(
        [d for d in dest_root.iterdir() if d.is_dir() and is_backup_dir(d.name)],
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )
    for old in all_backups[BACKUP_RETENTION:]:
        print(f"  Removing old backup: {old.name}")
        shutil.rmtree(old, ignore_errors=True)

    print(f"=== Backup completed successfully to: {target_dir} ===")


if __name__ == "__main__":
    main()

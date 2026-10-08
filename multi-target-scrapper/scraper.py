import hashlib
import json
import logging
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

import requests
import yaml
from bs4 import BeautifulSoup

DATA_DIR = "data"
STATE_FILE = f"{DATA_DIR}/state.json"
DB_FILE = f"{DATA_DIR}/history.db"
LOG_FILE = f"{DATA_DIR}/scraper.log"
CONFIG_FILE = "config.yaml"


# --------------------------------------------------------------------------- #
# Logging: stdout (docker logs) + fichero rotativo en el volumen
# --------------------------------------------------------------------------- #
def setup_logging() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    file_h = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_h.setFormatter(fmt)
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        handlers=[console, file_h],
    )


# --------------------------------------------------------------------------- #
# Histórico de matches (SQLite)
# --------------------------------------------------------------------------- #
def init_db() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_FILE) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS matches (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                first_seen TEXT NOT NULL,
                target_id  TEXT NOT NULL,
                url        TEXT NOT NULL,
                keyword    TEXT NOT NULL,
                line       TEXT NOT NULL,
                line_hash  TEXT NOT NULL,
                UNIQUE(target_id, line_hash)
            )
            """
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_matches_target ON matches(target_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_matches_kw ON matches(keyword)")


def record_matches(target: dict, found: list[tuple[str, str]]) -> list[str]:
    """Guarda (keyword, línea) en el histórico. Devuelve solo las líneas NUEVAS."""
    new_lines = []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DB_FILE) as c:
        for keyword, line in found:
            line_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()[:16]
            cur = c.execute(
                "INSERT OR IGNORE INTO matches "
                "(first_seen, target_id, url, keyword, line, line_hash) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (now, target["id"], target["url"], keyword, line[:300], line_hash),
            )
            if cur.rowcount == 1:
                new_lines.append(line)
    return new_lines


def find_matches(text: str, keywords: list[str]) -> list[tuple[str, str]]:
    if not keywords:
        return []
    # \b evita subcadenas como "política" al buscar "TIC"
    pattern = re.compile(
        r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", re.IGNORECASE
    )
    found = []
    for line in text.splitlines():
        m = pattern.search(line)
        if m:
            found.append((m.group(1).lower(), line.strip()))
    return found


# --------------------------------------------------------------------------- #
# Config / estado
# --------------------------------------------------------------------------- #
def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        logging.critical(f"Archivo base {CONFIG_FILE} no encontrado.")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(os.path.expandvars(f.read()))


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning("Corrupción en state.json. Inicializando tabla vacía.")
    return {}


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def send_telegram(token: str, chat_id: str, text: str) -> None:
    if not token or not chat_id or "TELEGRAM" in token:
        logging.error("Variables de entorno de Telegram no resueltas en el contenedor.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=10,
        ).raise_for_status()
        logging.info("Notificación enviada a Telegram.")
    except requests.RequestException as e:
        logging.error(f"Fallo de entrega HTTP a Telegram API: {e}")


# --------------------------------------------------------------------------- #
# Proceso por target
# --------------------------------------------------------------------------- #
def process_target(target: dict, state: dict, config: dict) -> dict:
    target_id = target["id"]
    name = target["name"]
    url = target["url"]
    selector = target["selector"]
    keywords = [k.lower() for k in target.get("keywords", [])]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    logging.info(f"Sondeando {name} ({url})")
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Fallo de sondeo en {name}: {e}")
        return state

    nodes = BeautifulSoup(resp.text, "html.parser").select(selector)
    if not nodes:
        logging.warning(
            f"Selector CSS '{selector}' estéril en {name}. Verifica cambios en el DOM."
        )
        return state

    extracted_text = "\n".join(n.get_text(strip=True) for n in nodes)
    current_hash = hashlib.sha256(extracted_text.encode("utf-8")).hexdigest()
    previous_hash = state.get(target_id, {}).get("hash")
    found = find_matches(extracted_text, keywords)

    if previous_hash is None:
        # Baseline: se registran los matches ya existentes sin notificar,
        # para que el primer cambio real no dispare un aluvión de avisos.
        record_matches(target, found)
        logging.info(
            f"Baseline para {name}: hash generado, {len(found)} coincidencias previas registradas."
        )
        state[target_id] = {"hash": current_hash}
        return state

    if current_hash == previous_hash:
        logging.info(f"Sin cambios en {name}.")
        return state

    new_matches = record_matches(target, found)
    logging.info(
        f"Divergencia de estado en {name}: {len(found)} coincidencias totales, "
        f"{len(new_matches)} nuevas."
    )
    for line in new_matches:
        logging.info(f"MATCH NUEVO [{target_id}] {line[:120]}")

    snippet = (
        "\n".join(new_matches[:5]) if new_matches else extracted_text[:250] + "..."
    )
    label = "Coincidencias nuevas" if new_matches else "Contenido (sin coincidencias nuevas)"
    send_telegram(
        config["telegram"]["bot_token"],
        config["telegram"]["chat_id"],
        f"🚨 *Cambio Detectado: {name}*\n\n🔗 [Acceder al Sitio]({url})\n\n📝 *{label}:*\n```{snippet}```",
    )
    state[target_id] = {"hash": current_hash}
    return state


def main():
    setup_logging()
    init_db()
    config = load_config()
    state = load_state()
    targets = config.get("targets", [])
    logging.info(f"Inicio de ciclo: {len(targets)} targets.")
    for target in targets:
        try:
            state = process_target(target, state, config)
        except Exception:
            # Un target roto no debe tumbar el resto del ciclo
            logging.exception(f"Error inesperado procesando {target.get('id')}")
    save_state(state)
    logging.info("Fin de ciclo.")


if __name__ == "__main__":
    main()
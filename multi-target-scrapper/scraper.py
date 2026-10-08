import hashlib
import json
import logging
import os
import re
import sys
from bs4 import BeautifulSoup
import requests
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

STATE_FILE = "data/state.json"
CONFIG_FILE = "config.yaml"

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        logging.critical(f"Archivo base {CONFIG_FILE} no encontrado.")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        # Interpolación explícita para resolver credenciales desde .env
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
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}, 
            timeout=10
        ).raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Fallo de entrega HTTP a Telegram API: {e}")

def process_target(target: dict, state: dict, config: dict) -> dict:
    target_id = target["id"]
    name = target["name"]
    url = target["url"]
    selector = target["selector"]
    keywords = [k.lower() for k in target.get("keywords", [])]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Fallo de sondeo en {name}: {e}")
        return state

    nodes = BeautifulSoup(resp.text, "html.parser").select(selector)
    if not nodes:
        logging.warning(f"Selector CSS '{selector}' estéril en {name}. Verifica cambios en el DOM.")
        return state

    extracted_text = "\n".join([n.get_text(strip=True) for n in nodes])
    current_hash = hashlib.sha256(extracted_text.encode("utf-8")).hexdigest()
    previous_hash = state.get(target_id, {}).get("hash")

    if previous_hash is None:
        logging.info(f"Generando hash baseline para {name}.")
        state[target_id] = {"hash": current_hash}
        return state

    if current_hash != previous_hash:
        matches = []
        if keywords:
            # Regex con límites de palabra (\b) para evitar subcadenas como "política" al buscar "TIC"
            pattern = re.compile(r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", re.IGNORECASE)
            for line in extracted_text.splitlines():
                if pattern.search(line):
                    matches.append(line.strip())

        snippet = "\n".join(matches[:5]) if matches else extracted_text[:250] + "..."
        
        logging.info(f"Divergencia de estado en {name}. Despachando evento...")
        send_telegram(
            config["telegram"]["bot_token"],
            config["telegram"]["chat_id"],
            f"🚨 *Cambio Detectado: {name}*\n\n🔗 [Acceder al Sitio]({url})\n\n📝 *Coincidencias (Regex):*\n```{snippet}```"
        )
        state[target_id] = {"hash": current_hash}

    return state

def main():
    config = load_config()
    state = load_state()
    for target in config.get("targets", []):
        state = process_target(target, state, config)
    save_state(state)

if __name__ == "__main__":
    main()
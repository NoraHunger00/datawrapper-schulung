import requests
import os
import time
from typing import Dict

CONFIG = {
    "datasets": {
        "hundebiss-statistik-2024-v2.csv": "https://www.berlin.de/sen/verbraucherschutz/aufgaben/hundehaltung/hundebiss-statistik/hundebiss-statistik-2024/2025-08-14-biss-statistik-2024.csv",
    },
    "output_dir": "./data",
    "create_dir": True,
    "verbose": True,
    "delay_seconds": 10,  # Längere Verzögerung
    "max_retries": 3,     # Maximale Wiederholungen
}

def download_file(url: str, output_path: str, verbose: bool = True, delay: int = 10, max_retries: int = 3) -> bool:
    """Lädt eine Datei mit Verzögerung, User-Agent und Retry-Logik herunter."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GitHub Actions Bot/1.0)"}
    for attempt in range(max_retries):
        try:
            if verbose:
                print(f"📥 Lade {os.path.basename(output_path)} von {url} (Versuch {attempt + 1}/{max_retries})...")
            time.sleep(delay * (attempt + 1))  # Verzögerung erhöht sich pro Versuch

            response = requests.get(url, stream=True, headers=headers)
            if response.status_code == 429:
                print(f"⚠️ 429 Too Many Requests. Warte {delay * (attempt + 2)} Sekunden...")
                continue
            response.raise_for_status()

            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            if verbose:
                print(f"✅ Erfolgreich heruntergeladen: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Herunterladen von {url} (Versuch {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                return False

def download_all_datasets(config: Dict) -> None:
    output_dir = config["output_dir"]
    datasets = config["datasets"]
    create_dir = config.get("create_dir", True)
    verbose = config.get("verbose", True)
    delay = config.get("delay_seconds", 10)
    max_retries = config.get("max_retries", 3)

    if create_dir:
        os.makedirs(output_dir, exist_ok=True)

    for filename, url in datasets.items():
        output_path = os.path.join(output_dir, filename)
        download_file(url, output_path, verbose, delay, max_retries)

if __name__ == "__main__":
    print(" Starte Daten-Download...")
    download_all_datasets(CONFIG)
    print(" Fertig!")

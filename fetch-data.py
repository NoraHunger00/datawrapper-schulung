import requests
import os
import time
from typing import Dict

# KONFIGURATION
CONFIG = {
    "datasets": {
        "hundebiss-statistik-2024.csv": "https://www.berlin.de/sen/verbraucherschutz/aufgaben/hundehaltung/hundebiss-statistik/hundebiss-statistik-2024/2025-08-14-biss-statistik-2024.csv",
    },
    "output_dir": "./data",
    "create_dir": True,
    "verbose": True,
    "delay_seconds": 5,  # 👈 Verzögerung zwischen den Requests
}

# HILFSFUNKTIONEN
def download_file(url: str, output_path: str, verbose: bool = True, delay: int = 5) -> bool:
    """Lädt eine Datei mit Verzögerung und User-Agent herunter."""
    try:
        if verbose:
            print(f"📥 Lade {os.path.basename(output_path)} von {url}...")

        time.sleep(delay)  # Verzögerung

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; GitHub Actions Bot/1.0)"
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if verbose:
            print(f"✅ Erfolgreich heruntergeladen: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Herunterladen von {url}: {e}")
        return False

def download_all_datasets(config: Dict) -> None:
    """Lädt alle in der Konfiguration definierten Datensätze herunter."""
    output_dir = config["output_dir"]
    datasets = config["datasets"]
    create_dir = config.get("create_dir", True)
    verbose = config.get("verbose", True)
    delay = config.get("delay_seconds", 5)

    if create_dir:
        os.makedirs(output_dir, exist_ok=True)

    for filename, url in datasets.items():
        output_path = os.path.join(output_dir, filename)
        download_file(url, output_path, verbose, delay)

# HAUPTPROGRAMM
if __name__ == "__main__":
    print("Starte Daten-Download...")
    download_all_datasets(CONFIG)
    print("Fertig!")
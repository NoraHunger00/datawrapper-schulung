import requests
import os
from typing import List, Dict


# KONFIGURATION
CONFIG = {
    # Liste der zu ladenden Datensätze
    # Format: {"dateiname": "URL"}
    "datasets": {
        "hundebiss-statistik-2024.csv": "https://www.berlin.de/sen/verbraucherschutz/aufgaben/hundehaltung/hundebiss-statistik/hundebiss-statistik-2024/2025-08-14-biss-statistik-2024.csv",
        # Weitere Datensätze können hier hinzugefügt werden, z. B.:
        # "bevoelkerung-2024.csv": "https://.../bevoelkerung-2024.csv",
    },
    # Ausgabeordner für die CSVs
    "output_dir":  os.path.expanduser("~/Documents/ODIS/Datawrapper Schulung/data"),
    # Soll der Ordner erstellt werden, falls er nicht existiert?
    "create_dir": True,
    # Soll eine Bestätigungsmeldung ausgegeben werden?
    "verbose": True,
}

# HILFSFUNKTIONEN
def download_file(url: str, output_path: str, verbose: bool = True) -> bool:
    """Lädt eine Datei von einer URL herunter und speichert sie lokal."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # HTTP-Fehler prüfen

        # Verzeichnis erstellen, falls nicht vorhanden
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Datei speichern
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

    if create_dir:
        os.makedirs(output_dir, exist_ok=True)

    for filename, url in datasets.items():
        output_path = os.path.join(output_dir, filename)
        if verbose:
            print(f"📥 Lade {filename} von {url}...")
        download_file(url, output_path, verbose)

# HAUPTPROGRAMM
if __name__ == "__main__":
    download_all_datasets(CONFIG)
    print("Datensätze wurden heruntergeladen. ")
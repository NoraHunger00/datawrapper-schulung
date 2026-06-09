import requests
import os
import time
import hashlib

# Konfiguration
DATA_URL = "https://www.berlin.de/sen/verbraucherschutz/aufgaben/hundehaltung/hundebiss-statistik/hundebiss-statistik-2024/2025-08-14-biss-statistik-2024.csv"
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "./data/hundebiss-statistik-2024.csv")

# 1. Prüfen, ob sich die Datei geändert hat
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "rb") as f:
        current_hash = hashlib.md5(f.read()).hexdigest()
else:
    current_hash = None

# 2. Daten herunterladen
print(f"📥 Lade Daten von Berlin.de in {OUTPUT_FILE}...")
headers = {"User-Agent": "Mozilla/5.0 (compatible; GitHub Actions Bot/1.0)"}

for attempt in range(3):
    try:
        time.sleep(10 * (attempt + 1))
        response = requests.get(DATA_URL, headers=headers)
        if response.status_code == 429:
            print(f"⚠️ 429 Too Many Requests (Versuch {attempt + 1}/3). Warte...")
            continue
        response.raise_for_status()

        new_content = response.content
        new_hash = hashlib.md5(new_content).hexdigest()

        # 3. Nur speichern, wenn sich die Daten geändert haben
        if current_hash and new_hash == current_hash:
            print("ℹ️ Daten haben sich nicht geändert. Überspringe Speichern und Upload.")
            exit(0)  # Beende das Skript, wenn keine Änderungen vorliegen

        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "wb") as f:
            f.write(new_content)
        print(f"✅ Daten erfolgreich gespeichert: {OUTPUT_FILE}")
        break
    except Exception as e:
        print(f"❌ Fehler beim Herunterladen (Versuch {attempt + 1}/3): {e}")
        if attempt == 2:
            print("❌ Maximale Versuche erreicht. Abbruch.")
            exit(1)

print("🎉 Fertig! Daten wurden aktualisiert.")
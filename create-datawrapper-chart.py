import requests
import os

# Konfiguration
api_key = os.getenv("DATAWRAPPER_API_KEY")
if not api_key:
    print("❌ DATAWRAPPER_API_KEY nicht gesetzt!")
    exit()

csv_file = os.getenv("CSV_FILE", "./data/hundebiss-statistik-2024.csv")
chart_id = "v6uXs"  # Deine Chart-ID

# 1. CSV laden (mit Fallback für verschiedene Kodierungen)
print(f"📥 Lade CSV aus {csv_file}...")
encoding_options = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
csv_text = None
for encoding in encoding_options:
    try:
        with open(csv_file, "r", encoding=encoding) as f:
            csv_text = f.read()
        print(f"✅ CSV erfolgreich mit Kodierung '{encoding}' geladen.")
        break
    except UnicodeDecodeError:
        continue

if not csv_text:
    print("❌ Konnte CSV mit keiner Kodierung laden!")
    exit()

# 2. Daten zu Datawrapper hochladen
print(f"📤 Lade Daten zu Chart {chart_id} hoch...")
update_response = requests.put(
    f"https://api.datawrapper.de/v3/charts/{chart_id}/data",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "text/csv"
    },
    data=csv_text
)

# 3. Ergebnis prüfen
if update_response.status_code in (200, 201, 204):
    print("✅ Daten erfolgreich hochgeladen!")
    print("🔗 Chart-URL:", f"https://www.datawrapper.de/_/{chart_id}")
else:
    print("❌ Fehler beim Hochladen der Daten:")
    print("Status:", update_response.status_code)
    print("Antwort:", update_response.text)
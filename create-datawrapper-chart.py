import requests
import os

# Konfiguration
api_key = os.getenv("DATAWRAPPER_API_KEY")
if not api_key:
    print("❌ DATAWRAPPER_API_KEY nicht gesetzt!")
    exit()

# 👇 Debug: API-Key prüfen (nur für Debugging!)
print(f"🔑 API-Key (erster und letzter Buchstabe): {api_key[0]}{'*' * (len(api_key) - 2)}{api_key[-1]}")
print(f"🔑 API-Key-Länge: {len(api_key)}")

csv_file = os.getenv("CSV_FILE", "./data/hundebiss-statistik-2024.csv")
chart_id = "v6uXs"  # Deine Chart-ID

# 1. CSV laden
print(f"📥 Lade CSV aus {csv_file}...")
with open(csv_file, "r", encoding="utf-8") as f:
    csv_text = f.read()

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
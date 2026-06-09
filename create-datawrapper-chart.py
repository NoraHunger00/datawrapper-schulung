import requests

# ======================
# 📌 KONFIGURATION
# ======================
api_key = "ht12LLqaQfZS6rbFVmvgQb8r8hBhPZYEKFhHeWkTuyO9wytTVsa922VPTkOoPJ2r"
csv_url = "https://raw.githubusercontent.com/NoraHunger00/datawrapper-schulung/main/data/hundebiss-statistik-2024.csv"

# 1. CSV von GitHub laden
print("📥 Lade CSV von GitHub...")
csv_response = requests.get(csv_url)
if csv_response.status_code != 200:
    print(f"❌ Fehler beim Laden der CSV: {csv_response.status_code}")
    exit()
csv_text = csv_response.text  # 👈 CSV als Text (nicht als Bytes!)

# 2. Chart erstellen
chart_title = "Hundebiss-Statistik Berlin 2024"
chart_type = "column-chart"

print("📊 Erstelle Chart...")
create_response = requests.post(
    url="https://api.datawrapper.de/v3/charts",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"title": chart_title, "type": chart_type}
)

if create_response.status_code != 201:
    print("❌ Fehler beim Erstellen des Charts:")
    print(create_response.json())
    exit()

chart_id = create_response.json()["id"]
print(f"✅ Chart erstellt mit ID: {chart_id}")

# 3. CSV als Text im Body des PUT-Requests senden
print("📤 Lade CSV-Daten hoch...")
update_response = requests.put(
    f"https://api.datawrapper.de/v3/charts/{chart_id}/data",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "text/csv"  # 👈 WICHTIG: Content-Type auf text/csv setzen!
    },
    data=csv_text  # 👈 CSV als Text im Body (nicht als JSON oder Datei!)
)

# 4. Ergebnis prüfen (PUT-Requests geben keine JSON-Antwort zurück)
if update_response.status_code in (200, 201, 204):
    print("✅ Daten erfolgreich hochgeladen!")
    print("🔗 Chart-URL:", f"https://www.datawrapper.de/_/{chart_id}")
    print("⚠️  Warte 1-2 Minuten, bis die Daten in Datawrapper angezeigt werden!")
else:
    print("❌ Fehler beim Hochladen der Daten:")
    print("Status:", update_response.status_code)
    print("Antwort:", update_response.text)
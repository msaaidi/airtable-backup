import os
import requests
import json
from datetime import datetime

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLES = [
    "Ein- und Auszahlungen",
    "Mohktar_Saaydi",
    "Mohammed_Laayoune",
    "khot_Mohammed_Schulden",
    "Kauf-Verkaufstabelle"
]

if not API_KEY or not BASE_ID:
    raise ValueError("Fehlende API-Key oder Base-ID Umgebungsvariablen.")

headers = {"Authorization": f"Bearer {API_KEY}"}

backup_folder = "backups"
os.makedirs(backup_folder, exist_ok=True)

for table in TABLES:
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        filename = f"{backup_folder}/{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Backup für '{table}' gespeichert: {filename}")
    else:
        print(f"❌ Fehler beim Abrufen von '{table}': {r.status_code} - {r.text}")

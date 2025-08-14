import os
import requests
import json
from datetime import datetime

# Airtable API Infos aus GitHub Secrets lesen
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Table 1")

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    raise ValueError("Fehlende API-Key oder Base-ID Umgebungsvariablen.")

# API URL
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# Header
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

# Daten abrufen
records = []
offset = None

while True:
    params = {}
    if offset:
        params["offset"] = offset

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    records.extend(data.get("records", []))

    offset = data.get("offset")
    if not offset:
        break

# Backup-Datei speichern
backup_filename = f"airtable_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
with open(backup_filename, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=4)

print(f"✅ Backup gespeichert als {backup_filename}")

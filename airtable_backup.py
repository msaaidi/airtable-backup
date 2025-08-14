import os
import requests
import json
from datetime import datetime

# Lade API-Key und Base-ID aus Umgebungsvariablen
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

def backup_table(table_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Backup erstellt: {filename}")

if __name__ == "__main__":
    for table in TABLES:
        backup_table(table)

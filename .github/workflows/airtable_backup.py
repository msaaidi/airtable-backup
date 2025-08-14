import requests
import pandas as pd
from datetime import datetime
import os

# === Konfiguration ===
API_KEY = "patTssJYKFxwil2cr"
BASE_ID = "appyjQzVUT4yQLvj6"
TABELLEN = [
    "Ein- und Auszahlungen",
    "Mohktar_Saaydi",
    "Mohammed_Laayoune",
    "khot_Mohammed_Schulden",
    "Kauf-Verkaufstabelle"
]
BACKUP_ORDNER = "backups"

# Sicherstellen, dass Backup-Ordner existiert
os.makedirs(BACKUP_ORDNER, exist_ok=True)

def fetch_airtable_records(table_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    all_records = []
    offset = None
    while True:
        params = {}
        if offset:
            params["offset"] = offset
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return all_records

today = datetime.now().strftime("%Y-%m-%d")

for table in TABELLEN:
    records = fetch_airtable_records(table)
    rows = [r["fields"] for r in records]
    df = pd.DataFrame(rows)
    backup_file = os.path.join(BACKUP_ORDNER, f"{table}_{today}.csv")
    df.to_csv(backup_file, index=False)
    print(f"Backup für {table} gespeichert: {backup_file}")
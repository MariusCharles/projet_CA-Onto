import os
import csv
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Charger la clé API NOAA
load_dotenv()
NOAA_TOKEN = os.getenv("NOAA_TOKEN")
if NOAA_TOKEN is None:
    raise ValueError("Clé API NOAA manquante dans .env")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def get_station_metadata(station_id):
    """Récupère les métadonnées d'une station NOAA via l'API"""
    url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/stations/GHCND:{station_id}"
    headers = {"token": NOAA_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Erreur API NOAA (station): {response.status_code} {response.text}")
    data = response.json()
    return {
        "id": station_id,
        "name": data.get("name", ""),
        "latitude": data.get("latitude", ""),
        "longitude": data.get("longitude", ""),
        "elevation": data.get("elevation", "")
    }

def fetch_noaa_data(station_id, start_date, end_date):
    """Télécharge les données NOAA pour une station entre deux dates"""
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    headers = {"token": NOAA_TOKEN}
    params = {
        "datasetid": "GHCND",
        "stationid": f"GHCND:{station_id}",
        "startdate": start_date,
        "enddate": end_date,
        "limit": 1000
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Erreur API NOAA: {response.status_code} {response.text}")
    return response.json().get("results", [])

def write_csv(station_meta, data, filename):
    """Crée un CSV au format attendu pour le script RDF"""
    fields = [
        "STATION","NAME","LATITUDE","LONGITUDE","ELEVATION",
        "DATE","PRCP","PRCP_ATTRIBUTES",
        "SNWD","SNWD_ATTRIBUTES",
        "TAVG","TAVG_ATTRIBUTES",
        "TMAX","TMAX_ATTRIBUTES",
        "TMIN","TMIN_ATTRIBUTES"
    ]

    rows_by_date = {}
    for entry in data:
        date = entry["date"][:10]
        dtype = entry["datatype"]
        value = entry.get("value", "")
        attr = entry.get("attributes", "")
        if date not in rows_by_date:
            rows_by_date[date] = {}
        rows_by_date[date][dtype] = (value, attr)

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for date, values in sorted(rows_by_date.items()):
            row = {
                "STATION": station_meta["id"],
                "NAME": station_meta["name"],
                "LATITUDE": station_meta["latitude"],
                "LONGITUDE": station_meta["longitude"],
                "ELEVATION": station_meta["elevation"],
                "DATE": date,
                "PRCP": values.get("PRCP", [""])[0],
                "PRCP_ATTRIBUTES": values.get("PRCP", ["",""])[1] if "PRCP" in values else "",
                "SNWD": values.get("SNWD", [""])[0],
                "SNWD_ATTRIBUTES": values.get("SNWD", ["",""])[1] if "SNWD" in values else "",
                "TAVG": values.get("TAVG", [""])[0],
                "TAVG_ATTRIBUTES": values.get("TAVG", ["",""])[1] if "TAVG" in values else "",
                "TMAX": values.get("TMAX", [""])[0],
                "TMAX_ATTRIBUTES": values.get("TMAX", ["",""])[1] if "TMAX" in values else "",
                "TMIN": values.get("TMIN", [""])[0],
                "TMIN_ATTRIBUTES": values.get("TMIN", ["",""])[1] if "TMIN" in values else "",
            }
            writer.writerow(row)

def fetch_and_save(station_id, start_date, end_date):
    station_meta = get_station_metadata(station_id)
    data = fetch_noaa_data(station_id, start_date, end_date)
    if not data:
        print(f"Aucune donnée pour {station_meta['name']} entre {start_date} et {end_date}")
        return
    filename = DATA_DIR / f"{station_id}_{start_date}_to_{end_date}.csv"
    write_csv(station_meta, data, filename)
    print(f"Données enregistrées dans : {filename}")

if __name__ == "__main__":
    # --- Récupération des arguments depuis Streamlit (ou CLI) ---
    if len(sys.argv) != 4:
        print("Usage: python get_data.py <station_id> <start_date> <end_date>")
        sys.exit(1)

    station_id = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    fetch_and_save(station_id, start_date, end_date)

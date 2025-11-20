import os
import csv
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
API_KEY = os.getenv("OWM_KEY")
if API_KEY is None:
    raise ValueError("Clé API OWM manquante dans .env")

# Dossier data
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Nom du CSV unique
CSV_FILE = DATA_DIR / "weather_all_cities.csv"

def get_weather(city):
    """Télécharge les données météo pour une ville"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "fr"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Erreur API pour {city} : {response.status_code} {response.text}")
        return None
    return response.json()

def append_to_csv(data, city):
    """Ajoute une ligne au CSV unique"""
    now = datetime.now()
    row = {
        "city": city,
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    }

    # Vérifier si le fichier existe déjà
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        fields = ["city", "datetime", "temperature", "humidity", "weather"]
        writer = csv.DictWriter(f, fieldnames=fields)
        if not file_exists:
            writer.writeheader()  # écrire les entêtes si fichier inexistant
        writer.writerow(row)

    return CSV_FILE

def fetch_and_append(city):
    """Télécharge et ajoute au CSV unique"""
    data = get_weather(city)
    if data:
        return append_to_csv(data, city)
    return None


if __name__ == "__main__":
    # Exemple : tester pour Paris
    city = "Paris"
    csv_file = fetch_and_append(city)
    if csv_file:
        print(f"Données ajoutées pour {city} dans : {csv_file}")
    else:
        print(f"Erreur pour {city}")

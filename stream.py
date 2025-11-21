import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import datetime 
from pathlib import Path
from streamlit_folium import st_folium
import folium
import os 
import requests
from dotenv import load_dotenv
from geopy.distance import geodesic


# Titre de la page
st.title("Interface météo")

####################################################
########## Affichage d'un pseudo-terminal ##########
####################################################

terminal = st.empty()

def stream_process(cmd):
    log = ""
    terminal.code(" ".join(cmd))
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        log += line
        terminal.code(log)
    process.wait()
    return process.returncode

###########################################################
########## Fonctions pour séléction de la station ##########
###########################################################

def download_all_stations(token, limit=1000):
    """
    Télécharge depuis l'API NOAA quelques stations météorologiques 
    pour les afficher sur la map
    """
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"
    headers = {"token": token}
    params = {
        "datasetid": "GHCND",
        "limit": limit,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        terminal.code(f"Erreur lors du téléchargement des stations (code {response.status_code})")
        return []

    data = response.json()
    return data.get("results", [])

def nearest_station(lat, lon, stations):
    """
    Calcul quelle est la station météo la plus proche
    """
    min_dist = float("inf")
    closest = None
    for s in stations:
        if "latitude" in s and "longitude" in s:
            dist = geodesic((lat, lon), (s["latitude"], s["longitude"])).km
            if dist < min_dist:
                min_dist = dist
                closest = s
    return closest

###############################################
########## Définition des paramètres ##########
###############################################

lat, lon = 48.8566, 2.3522 # par défaut coordonnées de Paris mais ne sont pas utilisés si pas de clic
station = "EI000003969" # par défaut les dates et la station sont choisis pour renvoyer des résultats valides
min_date = datetime.date(1763, 1, 1)
max_date = datetime.date.today()

start_date = st.date_input(
    "Date de début",
    value=datetime.date(2015, 11, 21),
    min_value=min_date,
    max_value=max_date
)

end_date = st.date_input(
    "Date de fin",
    value=datetime.date(2015, 11, 25),
    min_value=min_date,
    max_value=max_date
)

###########################################################################################
########## Création, affichage de la map et récupération des coordonnées du clic ##########
###########################################################################################

m = folium.Map(location=[lat, lon], zoom_start=5)

# Charger token NOAA
load_dotenv()
NOAA_TOKEN = os.getenv("NOAA_TOKEN")

# Télécharger les stations une seule fois et stocker dans session_state
if NOAA_TOKEN:
    if 'all_stations' not in st.session_state:
        terminal.code("Téléchargement des stations NOAA...")
        st.session_state.all_stations = download_all_stations(NOAA_TOKEN, limit=1000)
    all_stations = st.session_state.all_stations

    # Ajouter les stations sur la carte
    for s in all_stations:
        if "latitude" in s and "longitude" in s:
            folium.CircleMarker(
                location=[s["latitude"], s["longitude"]],
                radius=2,
                color="blue",
                fill=True,
                fill_opacity=0.8,
                tooltip=s.get("name", "Station")
            ).add_to(m)
else:
    terminal.code("Erreur : token NOAA introuvable")

# Afficher la carte et récupérer le clic
clicked_data = st_folium(m, width=700, height=500)

if clicked_data and clicked_data.get("last_clicked"):
    lat = clicked_data["last_clicked"]["lat"]
    lon = clicked_data["last_clicked"]["lng"]
    st.success(f"Coordonnées sélectionnées : lat={lat}, lon={lon}")

    folium.Marker([lat, lon], tooltip="Point sélectionné").add_to(m)

    # Recherche locale de la station la plus proche
    closest = nearest_station(lat, lon, st.session_state.all_stations)
    if closest:
        station = closest["id"].split(":")[1]
        terminal.code(f"Station la plus proche : {station} ({closest.get('name', 'Nom inconnu')})")
    else:
        terminal.code("Aucune station trouvée proche du clic.")
else:
    st.info("Cliquez sur la carte pour sélectionner un point.")

###########################################
########## Téléchargement du CSV ##########
###########################################

if st.button("1- Télécharger CSV"):
    if not station:
        st.error("Veuillez indiquer le numéro de la station.")
    else:
        ret = stream_process(["python", "get_data.py", str(station), str(start_date), str(end_date)])
        csv_filename = f"data/{station}_{start_date}_to_{end_date}.csv"
        csv_path = Path(csv_filename)
        if csv_path.exists():
            st.success(f"CSV téléchargé avec succès !\nFichier : {csv_filename}")
        else:
            st.error("Le téléchargement a échoué : le fichier CSV n'a pas été créé.")

########################################
########## Génération du .RDF ##########
########################################

if st.button("2- Générer RDF"):
    ret = stream_process(["python", "generate_rdf.py", str(station), str(start_date), str(end_date)])
    rdf_filename = "data/weather.rdf"
    rdf_path = Path(rdf_filename)
    if rdf_path.exists():
        st.success(f"RDF créé avec succès !\nFichier : {rdf_filename}")
    else:
        st.error("La création a échoué : le fichier RDF n'a pas été créé.")

#########################################################################
########## Création et affichage du graphique des Températures ##########
#########################################################################

if st.button("3- Afficher graphiques températures"):
    rdf_path = Path("data/weather.rdf")
    img_path = Path("data/temperature_plot.png")
    if not rdf_path.exists():
        st.error("Fichier RDF introuvable. Veuillez d'abord générer le RDF.")
    else:
        ret = stream_process(["python", "graph_temp.py", str(rdf_path), str(img_path)])
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.error("Le graphique n'a pas pu être généré.")

###########################################################################
########## Création et affichage du graphique des Précipitations ##########
###########################################################################

if st.button("4- Afficher graphiques précipitation"):
    rdf_path = Path("data/weather.rdf")
    img_path = Path("data/precipitation_plot.png")
    if not rdf_path.exists():
        st.error("Fichier RDF introuvable. Veuillez d'abord générer le RDF.")
    else:
        ret = stream_process(["python", "graph_precip.py", str(rdf_path), str(img_path)])
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.error("Le graphique n'a pas pu être généré.")

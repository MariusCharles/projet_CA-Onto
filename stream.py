import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import datetime 
from pathlib import Path

# Titre de la page
st.title("Interface météo")

# Paramètres à rentrer par l'utilisateur
station = st.text_input("Numéro de station")
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
# Télécharger le csv
if st.button("1- Télécharger CSV"):
    if not station:
        st.error("Veuillez indiquer le numéro de la station.")
    else:
        # Appel de ton script Python pour télécharger CSV
        subprocess.run(["python", "get_data.py", str(station), str(start_date), str(end_date)])
        # Vérifier si le fichier a été créé
        csv_filename = f"data/{station}_{start_date}_to_{end_date}.csv"
        csv_path = Path(csv_filename)
        if csv_path.exists():
            st.success(f"CSV téléchargé avec succès !\nFichier : {csv_filename}")
        else:
            st.error("Le téléchargement a échoué : le fichier CSV n'a pas été créé.")

# Générer le fichier RDF
if st.button("2- Générer RDF"):
    # Appel de ton script de transformation CSV → RDF
    subprocess.run(["python", "generate_rdf.py",str(station), str(start_date), str(end_date)])
    rdf_filename = "data/weather.rdf"
    rdf_path = Path(rdf_filename)
    if rdf_path.exists():
        st.success(f"RDF créé avec succès !\nFichier : {rdf_filename}")
    else:
         st.error("La création a échoué : le fichier RDF n'a pas été créé.")

# Affichage du Graphiques des Températures min et max
if st.button("3- Afficher graphiques températures"):
    rdf_path = Path("data/weather.rdf")
    img_path = Path("data/temperature_plot.png")
    if not rdf_path.exists():
        st.error("Fichier RDF introuvable. Veuillez d'abord générer le RDF.")
    else:
        subprocess.run(["python", "graph_temp.py", str(rdf_path), str(img_path)])
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.error("Le graphique n'a pas pu être généré.")


# Affichage du Graphique des Précipitations
if st.button("4- Afficher graphiques précipitation"):
    rdf_path = Path("data/weather.rdf")
    img_path = Path("data/precipitation_plot.png")
    if not rdf_path.exists():
        st.error("Fichier RDF introuvable. Veuillez d'abord générer le RDF.")
    else:
        subprocess.run(["python", "graph_precip.py", str(rdf_path), str(img_path)])
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.error("Le graphique n'a pas pu être généré.")

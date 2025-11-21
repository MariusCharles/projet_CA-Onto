# projet_CA-Onto

# Interface météo - Projet CA-Onto

Ce projet est une interface interactive pour explorer des données météorologiques et les transformer en RDF à l'aide de l'ontologie **CA Ontology**.  
Il a été réalisé dans le cadre d'un projet d'évaluation pour un cours d'introduction aux ontologies et au Web sémantique.

Le fichier de transformation CSV → RDF est largement inspiré du travail de **J. Wu, F. Orlandi, D. O'Sullivan, S. Dev, "An Ontology Model for Climatic Data Analysis, under review"**, qui a créé l'ontologie CA utilisée dans ce projet.

## Fonctionnalités

- Sélection de période : date de début et date de fin pour les données météorologiques.
- Carte interactive : cliquer pour sélectionner un point et récupérer la station la plus proche.
- Téléchargement CSV : récupérer les données météo pour la station et la période sélectionnées.
- Génération RDF : transformer le CSV en RDF selon la CA Ontology.
- Visualisation : afficher les graphiques des températures et des précipitations basés sur les données RDF.

> Note : Par défaut, si aucune date n’est modifiée et aucun clic n’est fait, les variables sont initialisées pour renvoyer des données valides. Certaines stations n’ont pas de données pour toutes les dates, il peut être nécessaire d’essayer plusieurs combinaisons.

## Structure du projet
```
projet_CA-Onto/
├─ data/
│ ├─ <station>_<start>to<end>.csv
│ ├─ weather.rdf
│ ├─ temperature_plot.png
│ └─ precipitation_plot.png
├─ get_data.py
├─ generate_rdf.py
├─ graph_temp.py
├─ graph_precip.py
├─ app.py
├─ .env
└─ README.md
```


## Installation

1. Cloner le dépôt :

```bash
git clone <URL_DU_REPO>
cd projet_CA-Onto
```

2. Installer les dépendances Python :

```bash
pip install streamlit pandas matplotlib folium streamlit-folium requests python-dotenv geopy
```

3. Ajouter votre token NOAA dans un fichier .env à la racine du projet :
```bash
NOAA_TOKEN=VOTRE_TOKEN_ICI
```

## Utilisation


Sur la page :

1. Sélectionner les dates de début et de fin si nécessaire.
2. Cliquer sur la carte pour choisir une station proche du point désiré.
3. Utiliser les boutons pour :
   - Télécharger le CSV
   - Générer le RDF
   - Afficher les graphiques des températures
   - Afficher les graphiques des précipitations

## Remarques

- Le projet utilise **CA Ontology** pour structurer les données RDF.
- Le pseudo-terminal intégré affiche les logs en direct lors de l’exécution des scripts.
- Certaines stations n’ont pas de données pour toutes les dates. Il peut être nécessaire d’essayer plusieurs combinaisons.

  > Note : La page peut légèrement se figer pendant quelques instants en raison des interactions avec l'API NOAA.

  






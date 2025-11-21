import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

st.title("Interface météo")

# --- Paramètres de base ---
station = st.text_input("Numéro de station")
start_date = st.date_input("Date de début")
end_date = st.date_input("Date de fin")

# --- Bouton 1 : Télécharger CSV ---
if st.button("1️⃣ Télécharger CSV"):
    if not station:
        st.error("Veuillez indiquer le numéro de la station.")
    else:
        # Appel de ton script Python pour télécharger CSV
        subprocess.run(["python", "scripts/download.py", str(station), str(start_date), str(end_date)])
        st.success("CSV téléchargé avec succès !")

# --- Bouton 2 : Générer RDF ---
if st.button("2️⃣ Générer RDF"):
    # Appel de ton script de transformation CSV → RDF
    subprocess.run(["python", "scripts/csv_to_rdf.py"])
    st.success("RDF généré avec succès !")

# --- Bouton 3 : Afficher graphiques températures ---
if st.button("3️⃣ Afficher graphiques températures"):
    df_temp = pd.read_csv("data/temperature.csv")  # ton CSV
    st.subheader("Températures")
    fig, ax = plt.subplots()
    ax.plot(df_temp['date'], df_temp['min'], label="Min")
    ax.plot(df_temp['date'], df_temp['max'], label="Max")
    ax.set_xlabel("Date")
    ax.set_ylabel("Température")
    ax.legend()
    st.pyplot(fig)
    st.dataframe(df_temp)

# --- Bouton 4 : Afficher graphiques précipitations ---
if st.button("4️⃣ Afficher graphiques précipitations"):
    df_precip = pd.read_csv("data/precipitation.csv")  # ton CSV
    st.subheader("Précipitations")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_precip['date'], df_precip['value'])
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Précipitation")
    st.pyplot(fig2)
    st.dataframe(df_precip)


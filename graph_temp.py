from rdflib import Graph
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le fichier RDF
g = Graph()
g.parse("data/weather.rdf", format="xml")

# Requête SPARQL pour toutes les observations de température
query = """
PREFIX classe: <http://example.org/ca/ont/Class/>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX qudt: <http://qudt.org/1.1/schema/qudt#>

SELECT ?date ?minval ?maxval
WHERE {
     ?obs a classe:TemperatureObservation ;
         sosa:resultTime ?date ;
         sosa:hasResult ?min , ?max .

      ?min a classe:TemperatureResult ;
           rdfs:label "min" ;
           qudt:numericValue ?minval .

      ?max a classe:TemperatureResult ;
           rdfs:label "max" ;
           qudt:numericValue ?maxval
}
ORDER BY ?date
"""

# Stocker les résultats
dates = []
min_vals = []
max_vals = []

for row in g.query(query):
    dates.append(datetime.strptime(str(row.date), "%Y-%m-%d"))
    min_vals.append(float(row.minval))
    max_vals.append(float(row.maxval))

# Créer le graphique
plt.figure(figsize=(10,5))
plt.plot(dates, min_vals, marker='o', linestyle='-', color='blue', label='Min Temp')
plt.plot(dates, max_vals, marker='o', linestyle='-', color='red', label='Max Temp')
plt.title("Températures min et max par date")
plt.xlabel("Date")
plt.ylabel("Température (°F)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

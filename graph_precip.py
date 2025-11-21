from rdflib import Graph
import matplotlib.pyplot as plt
from datetime import datetime

# Charger le fichier RDF
g = Graph()
g.parse("data/weather.rdf", format="xml")

# Requête SPARQL pour toutes les observations de précipitations
query = """
PREFIX classe: <http://example.org/ca/ont/Class/>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX qudt: <http://qudt.org/1.1/schema/qudt#>

SELECT ?date ?val
WHERE {
     ?obs a classe:PrecipitationObservation ;
          sosa:resultTime ?date ;
          sosa:hasResult ?precipitation .

     ?precipitation a classe:PrecipitationResult ;
                    qudt:numericValue ?val .
}
ORDER BY ?date
"""

# Stocker les résultats
dates = []
values = []

for row in g.query(query):
    # Convertir la date string en objet datetime
    dates.append(datetime.strptime(str(row.date), "%Y-%m-%d"))
    values.append(float(row.val))

# Créer le graphique
plt.figure(figsize=(10,5))
plt.plot(dates, values, marker='o', linestyle='-', color='blue')
plt.title("Précipitations par date")
plt.xlabel("Date")
plt.ylabel("Précipitation (inch)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

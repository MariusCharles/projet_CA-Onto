# graph_temp.py
import sys
from rdflib import Graph
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if len(sys.argv) != 3:
    print("Usage: python graph_temp.py <rdf_file> <output_image>")
    sys.exit(1)

rdf_file = sys.argv[1]
output_image = sys.argv[2]

g = Graph()
g.parse(rdf_file, format="xml")

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

dates, min_vals, max_vals = [], [], []

for row in g.query(query):
    dates.append(datetime.strptime(str(row.date), "%Y-%m-%d"))
    min_vals.append(float(row.minval))
    max_vals.append(float(row.maxval))

if not dates:
    print("Aucune donnée de température trouvée.")
else:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(dates, min_vals, marker='o', linestyle='-', color='blue', label='Min Temp')
    ax.plot(dates, max_vals, marker='o', linestyle='-', color='red', label='Max Temp')
    ax.set_xlabel("Date")
    ax.set_ylabel("Température (°F)")
    ax.set_title("Températures min et max par date")
    ax.legend()
    ax.grid(True)

    # Formater les dates pour l'axe x
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # choix automatique des ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # format AAAA-MM-JJ
    fig.autofmt_xdate(rotation=45)  # rotation pour lisibilité

    plt.tight_layout()
    fig.savefig(output_image)
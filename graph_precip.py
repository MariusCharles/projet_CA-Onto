# graph_precip.py
import sys
from rdflib import Graph
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if len(sys.argv) != 3:
    print("Usage: python graph_precip.py <rdf_file> <output_image>")
    sys.exit(1)

rdf_file = sys.argv[1]
output_image = sys.argv[2]

g = Graph()
g.parse(rdf_file, format="xml")


# Requête SPARQL 
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


dates = []
values = []

for row in g.query(query):

    dates.append(datetime.strptime(str(row.date), "%Y-%m-%d"))
    values.append(float(row.val))



if not dates:
    print("Aucune donnée de précipitation trouvée.")
else:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(dates, values, marker='o', linestyle='-', color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Précipitation (mm)")
    ax.set_title("Précipitation par date")
    ax.grid(True)

    # Formater les dates pour l'axe x
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # format AAAA-MM-JJ
    fig.autofmt_xdate(rotation=45)  

    plt.tight_layout()
    fig.savefig(output_image)
#Importations des fonctionnalités
import requests #Envoi les requêtes
from bs4 import BeautifulSoup #Bibliothèque Python
import pandas as pd #Bibliothèque python pour la mise en tableau de données

#Recupération de la page principal
req = requests.get("https://www.frameip.com/liste-des-ports-tcp-udp/")
req.text

#Création de "soup" principale
soup = BeautifulSoup(req.content)

#Récupération de la liste des liens
entry_content = soup.find("div", {"class": "entry-content"})
link_list = entry_content.find_all("ul")[-1]
url_list = [a["href"] for a in link_list.find_all("a")]

print(url_list)

#Récupération des pages web
plage_reqs = []
for url in url_list:
  print(f"[+] Requête ver {url}...")
  req = requests.get(url)
  plage_reqs.append(req)

#Création des soupes
soups = [BeautifulSoup(req.content) for req in plage_reqs]

#Récupération de la balise représentant le tableau de ports pour chaque soupes
ports_tables = [soup.find("table") for soup in soups]

#Récupérations des lignes des tableaux de ports
table_lines = []
for table in ports_tables:
  lines = table.find_all("tr")[1:]
  table_lines += lines

len(table_lines)

#Pour chaque ligne du tableau, récupérer les balises "td"
ports_info = []
for line in table_lines:
  cells = line.find_all("td")
  port_name = cells[0].text.strip()
  port_number = cells[1].text.strip()
  port_protocol = cells[2].text.strip()
  port_description = cells[3].text.strip()
  ports_info.append({
      "name": port_name,
      "number": port_number,
      "protocol": port_protocol,
      "description": port_description
  })

print(ports_info)

#Création des ports en tant que clés
data = {}
for info in ports_info:
  data[info["number"]] = {}

print(data)

#Création des protocols en tant que clés
for info in ports_info:
  data[info["number"]][info["protocol"]] = {}

print(data)

#Association des noms aux descriptions des ports données pour le protocol donné
for info in ports_info:
  data[info["number"]][info["protocol"]][info["name"]] = info["description"]

print(data)

#Affichage des données sous forme de tableau grâce à "Pandas"
pd.DataFrame.from_dict(data, orient='index')



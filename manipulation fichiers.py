#écriture

import csv

with open('grh.csv') as fichier_csv:
    reader = csv.DictReader(fichier_csv, delimiter=',')
    for ligne in reader:
        print(ligne['nom'] + " a travaillé " + ligne['heures']+ " heures")
        

# Créer une liste pour les en-têtes
    en_tete = ["titre", "description"]

    # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv »
    with open('data.csv', 'w') as fichier_csv:
        # Créer un objet writer (écriture) avec ce fichier
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        liste=["ajllj","lklklk","lllkkk","iioppaiej"]
        # Parcourir les titres et descriptions - zip permet d'itérer sur deux listes ou plus à la fois
        for a in liste:
            # Créer une nouvelle ligne avec le titre et la description à ce moment de la boucle
           
            writer.writerow(a)
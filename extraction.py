import requests

from bs4 import BeautifulSoup
with open("pageweb.html", 'r') as file:

    soup = BeautifulSoup(file, 'html.parser')

    title=soup.title.string
    h1_text=soup.h1.string

    products = soup.find_all('li')
    laliste=[]
    for product in products:
        name=product.h2.string
        price = product.find('p', string=lambda s: 'Prix' in s).string
        laliste.append((name,price))

    print(laliste)

# Extraction des descriptions des produits dans la liste
descriptions_list = []
for product in products:
    description = product.find('p', string=lambda s: 'Description' in s).string
    descriptions_list.append(description)

# Étape 2 : Affichage des informations extraites
print("Titre de la page :", title)
print("Texte de la balise h1 :", h1_text)
print("Liste des produits :", laliste)
print("Liste des descriptions de produits :", descriptions_list)
    
""""
    listetitre=[]
    for t in x:
        listetitre.append(t.string)

    print (listetitre)
#for t in listetitre:
#    print(t)

"""

import requests
import math
import os
from bs4 import BeautifulSoup

def extraction_csv (categorie,premiere_page,derniere_page,index_cat):

    page=1
    page=int(page)
    listelivre=[]
    notation=["One","Two","Three","Four","Five"]
    prices=["prix"]
    titres=["titre"]
    dispo=["dispo"]
    rating=["note"]
    liens=["lien"]
    categories=[]
    serie_totale=[]
    listecat=["Fiction","Art"]

# BOUCLE POUR EXTRACTIONS SOUS FORME DE LISTE DES ELEMENTS - la boucle couvre les pages choisies ( a à b) pour
# la catégorie (trois paramètres de la fonction)
    for boucle in range (premiere_page,derniere_page):
        
        url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(index_cat)+"/page-"+str(boucle)+".html"

        print(url)
        print(f"BOUCLE # {boucle}")
        contenu = requests.get(url)
            
        soup = BeautifulSoup(contenu.text,"html.parser")
    
    # je récupère toutes les sous parties     
        tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        #print(tous)
    #puis je traite chaque sous parties pour en extraire titre, lien, prix..
    #...que j'ajoute à des listes
        for livre in tous:
                titres.append(livre.find("img").attrs["alt"])
                print (livre.find("img").attrs["alt"])
        print(titres)
 #je compose une liste contenant les éléments pour chaque bouquin (format csv en colonnes avec virgule)
        for j in range((boucle*20),(boucle+1)*20): 
            print ("SOUS BOUCLE"+str(j)) 
            print(str(j)+","+titres[j])
   
   # serie_totale.insert(0,"titre,prix,disponible,lien,note") 


extraction_csv("Fiction",1,2,10)
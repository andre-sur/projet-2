import tkinter as tk
import requests
import math
import os
import shutil
from bs4 import BeautifulSoup
from tkinter import messagebox

def extraction_ciblee(x,y,z):
    validation=tk.Tk()
    validation.title("Validation")
    validation.geometry("400x200")

    label=tk.Label(validation,text=f"Extraction de la catégorie {x}, pages : {y} à {z}")
    label.pack(pady=5)
    #last_one=tk.Button(validation,text="Valider",command=extraction_csv(x,y,z))
   
    #last_one.pack(pady=5)
    total_livres=nombre_livre(x)
    extraction_csv(x,y,z,nom_fichier=x+"_page"+str(y)+"to"+str(z),maxbook=total_livres)
    validation.mainloop()

def extraire_toutes ():
    if not os.path.exists("Par categories"):
        os.makedirs("Par categories")
    clonelist=listecat.copy()
    del clonelist[0]
    del clonelist[0]
    print(listecat)
    for categorie_en_cours in clonelist:
    #categorie_en_cours="Fantasy"
        maxbook=nombre_livre(categorie_en_cours)
        maximus=math.ceil(maxbook/20)
        print(categorie_en_cours+" - MAX PAGE "+str(maximus)+" et nbre bouquin "+str(maxbook))
        extraction_csv(categorie_en_cours,1,maximus,categorie_en_cours,maxbook)

def nombre_livre(choix):
    #global abc

    #choix=var_1.get()
    if choix=="Tous":
        url_base="https://books.toscrape.com/index.html"
    elif choix in listecat :
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(listecat.index(choix))+"/index.html"
    else:
        url_base="https://books.toscrape.com/index.html" 

    etape1 = requests.get(url_base)
    etape2 = BeautifulSoup(etape1.text,"html.parser")
    trouve_strong=etape2.find_all("strong")

    strong_liste=[]
    for i in trouve_strong:
        strong_liste.append(i.text)
    total_livres=int(strong_liste[1])
    return(total_livres)

def check_ok():
    try :
        v2=int(var_2.get())
        v3=int(var_3.get())

        if v2>v3 :
            messagebox.showinfo("ERREUR","Nombre trop élévé ou incohérence")
        else:
            v1=var_1.get()
            v2=int(var_2.get())
            v3=int(var_3.get())
            extraction_ciblee(v1,v2,v3)
    except ValueError:
            messagebox.showinfo("Erreur","Entrez uniquement des nombres")

def recupere_photos ():
    nbre_page=40 
    liens=[]
    tous=[]
    url_image=""
    if not os.path.exists("Images"):
        os.makedirs("Images")
    print("nombre de pasge début boucle extract"+str(nbre_page))

    for boucle in range (1,nbre_page):
       
        url="https://books.toscrape.com/catalogue/page-"+str(boucle)+".html"

        contenu = requests.get(url)
        soup=BeautifulSoup(contenu.text,"html.parser")
        
        tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        print(url)  
        print(tous) 
        
       # src_value=img_tag["src"]
       
        #soup = BeautifulSoup(contenu.text,"html.parser")
        #tous=soup.find_all("a",img_="src")
        #print(tous)
        for livre in tous:   
            liens.append("https://books.toscrape.com/"+livre.find("img").attrs["src"][3:])
            
            
        #img_tag=soup.find("img")
         #   src_value=livre["src"]
          #  print(src_value)
            
            #print((livre.find("a").attrs["href"]))

        print(liens)

        for variable in range (0,len(liens)):
            url_image=liens[variable]
            print(url_image)
            response=requests.get(url_image,stream=True)
            if response.status_code==200:
                with open (os.path.join("Images","image"+str(variable)+".jpg"),"wb") as file:
             #
                    shutil.copyfileobj(response.raw, file)
                print("image sauvée ok")
                
            else : 
                print ("Impossible de télécharger")



#Fonction pour créer un fichier csv formaté à partir des choix faits (catégorie, quelles pages extraire)
def extraction_csv (categorie,premiere_page,derniere_page,nom_fichier,maxbook):

    nbre_page=derniere_page-premiere_page+1
    print(nom_fichier+"total bouquin"+str(maxbook))
    listelivre=[]
    serie_totale=[]
    notation=["One","Two","Three","Four","Five"]
    prices=[]
    titres=[]
    dispo=[]
    rating=[]
    liens=[]
   
    categories=[]
    #serie_totale=["titre,prix,dispo,lien,note"]
    print("nombre de pasge début boucle extract"+str(nbre_page))
# BOUCLE POUR EXTRACTIONS SOUS FORME DE LISTE DES ELEMENTS - la boucle couvre les pages choisies ( a à b) pour
# la catégorie (trois paramètres de la fonction)
    for boucle in range (1,nbre_page+1):
        print("boucle " + str(boucle))
        print("CATEGORIE"+str(listecat.index(categorie)))
        if boucle==1:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(listecat.index(categorie))+"/index.html"

        else:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(listecat.index(categorie))+"/page-"+str(boucle)+".html"

        print(url)
        print(boucle)
        contenu = requests.get(url)
            
        soup = BeautifulSoup(contenu.text,"html.parser")
    
    # je récupère toutes les sous parties     
        tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        #print(tous)
    #puis je traite chaque sous parties pour en extraire titre, lien, prix..
    #...que j'ajoute à des listes
        for livre in tous:
                
                titres.append(livre.find("img").attrs["alt"])
                liens.append("https://books.toscrape.com/"+livre.find("img").attrs["src"][3:])
                prices.append(livre.find("p", class_="price_color").text[2:])
                dispo.append(livre.find("p", class_="instock availability").text.strip())

#Récupérer et ajouter le rating (traitement spécifique)
                les_balises_p=livre.find_all("p")
        #On extrait la note des balises p : c'est la seconde de la liste donc [1]       
                for z in les_balises_p : 
                    try : 
                        z.get("class",[])[1]
                        if z.get("class",[])[1] in notation:
                            y=z.get("class",[])[1]
                            rating.append(y)
                        else:
                            pass
                                
                    except IndexError:
                        pass

    print(titres)
    print(maxbook)
 #je compose une liste contenant les éléments pour chaque bouquin (format csv en colonnes avec virgule)
    for j in range(0,maxbook):
        print(j)
        serie_totale.append(titres[j]+","+prices[j]+","+dispo[j]+","+liens[j]+","+rating[j])
        print("   AAAA"+str(j)+"  "+titres[j]+","+prices[j]+","+dispo[j]+","+liens[j]+","+rating[j])
    #print(serie_totale)

                          
#j'écris un fichier csv avec pour chaque ligne titre et prix séparés par virgule et un header (1ère ligne) titre,prix
    with open(os.path.join("Par categories",nom_fichier+".csv"),"w", encoding="utf-8") as fichier:
        #os.mkdir(categorie)
        for z in range(1,maxbook):
            print ("z     "+str(z))
            print(serie_totale[z]+"\n")
            temporaire=serie_totale[z]+"\n"
            fichier.write(temporaire)
        


#une fois le choix fait de la catégorie et des pages à extraire, on demande confirmation 
# puis on appelle la fonction extraction_csv pour écrire un fichier csv
#quand l'utilisateur modifie la sélection de la catégorie, on met à jour nbre de pages correspondant

def calcul_maxpage(var_name,index,mode):
    #global abc

    choix=var_1.get()
    if choix=="Tous":
        url_base="https://books.toscrape.com/index.html"
    elif choix in listecat :
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(listecat.index(choix))+"/index.html"
    else:
        url_base="https://books.toscrape.com/index.html" 

    etape1 = requests.get(url_base)
    etape2 = BeautifulSoup(etape1.text,"html.parser")
    #trouver le nombre total de livres...
    trouve_strong=etape2.find_all("strong")

    strong_liste=[]
    #...pour en déduire le nombre total de pages (avec 20 livres par page)
    for i in trouve_strong:
        strong_liste.append(i.text)
    nbre_page=math.ceil(int(strong_liste[1])/20)

    #abc=nbre_page
    label_var.set(f"Pour cette catégorie, il y a au total {nbre_page} pages")
    #return(nbre_page)
    
    return(nbre_page)

#DEBUT DU PROGRAMME PRINCIPAL - MENU AVEC CATEGORIE ET FENETRE Entrée nbre de pages

root=tk.Tk()
root.title("Menus dépendants")
root.geometry("300x400")

# o CATEGORIES

url = "https://books.toscrape.com/catalogue/page-1.html"
contenu = requests.get(url)
soupe = BeautifulSoup(contenu.text,"html.parser")

#EXTRACTION DES CATEGORIES
totale=soupe.find_all("ul",class_="nav nav-list")
        #print (tous)
#print (menu)
listecat=[]

for i in totale:
    listecat=i.get_text(separator=",",strip=True).split(",")

listecat.insert(0,"Tous")
 
var_1=tk.StringVar(root)
var_2=tk.StringVar(root)
var_3=tk.StringVar(root)
label_var=tk.StringVar()

menu_1=tk.OptionMenu(root,var_1,*listecat)
menu_1.pack(pady=10)

etik1=tk.Label(root,text="Extraction à partir de la page :")
etik1.pack(pady=10)

var_2=tk.Entry(root, width=10)
var_2.insert(0,"1")
var_2.pack(pady=10)

etik2=tk.Label(root,text="Et jusqu'à la page :")
etik2.pack(pady=10)
var_3=tk.Entry(root, width=10)
var_3.insert(0,"1")
var_3.pack(pady=10)


var_1.trace_add("write",calcul_maxpage)


label2=tk.Label(root,textvariable=label_var)
label2.pack(pady=10)

valider=tk.Button(root,text="Valider",command=check_ok)
valider.pack(pady=10)

extraire_toutes_categories=tk.Button(root,text="Extraire toutes les catégories",command=extraire_toutes)
extraire_toutes_categories.pack(pady=10)

extraire_photos=tk.Button(root,text="Extraire toutes les photos",command=recupere_photos)
extraire_photos.pack(pady=10)

#valider=tk.Button(root,text="Extraire chaque catégorie et enregistrer csv",command=extraction_toutes())
#valider.pack(pady=10)


root.mainloop()
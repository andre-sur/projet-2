

import tkinter as tk
import requests
import math
from bs4 import BeautifulSoup
from tkinter import messagebox

#Fonction pour créer un fichier csv formaté à partir des choix faits (catégorie, quelles pages extraire)
def extraction_csv (categorie,a,b):

    page=1
    page=int(page)
    listelivre=[]
    a=1
    b=4
    notation=["One","Two","Three","Four","Five"]
    seria=[]
    prices=[]
    titres=[]
    dispo=[]
    rating=[]
    liens=[]
    categories=[]
    serie_totale=[]

    # BOUCLE POUR EXTRACTIONS SOUS FORME DE LISTE DES ELEMENTS - la boucle couvre les (n) pages choisies
    for x in range (a,b):
        
        url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(listecat.index(categorie))+"/index.html"

        print(url)
        contenu = requests.get(url)
            
        soupe = BeautifulSoup(contenu.text,"html.parser")
            #categorie= categorie_0.text[0:soupe.title.text.index("|")]
                
        tous=soupe.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        print (tous)
            
        for livre in tous:
                
                titres.append(livre.find("img").attrs["alt"])
                liens.append(livre.find("a").attrs["href"])
                prices.append(livre.find("p", class_="price_color").text[2:])
                dispo.append(livre.find("p", class_="instock availability").text.strip())

#Récupérer et ajouter le rating
                touslesps=livre.find_all("p")
                    
                for z in touslesps : 
        
                    try : 
                        z.get("class",[])[1]
                        if z.get("class",[])[1] in notation:
                            y=z.get("class",[])[1]
                            rating.append(y)
                        else:
                            pass
                                
                    except IndexError:
                        pass
                        
                        

                        
                        
 #je compose une liste contenant les éléments pour chaque bouquin
        for j in range(1+(x-1)*20,len(tous)+(x-1)*20):
                    
            serie_totale.append(titres[j]+","+prices[j]+","+dispo[j]+","+liens[j]+","+rating[j])
    serie_totale.insert(0,"titre,prix,disponible,lien,note")                    


#j'écris un fichier csv avec pour chaque ligne titre et prix séparés par virgule et un header titre,prix
    with open("extraction.csv","w") as f:
        for j in range(0,len(serie_totale)):
            f.write (f"{serie_totale[j]}\n")
            f.close


    print(serie_totale)


#une fois le choix fait de la catégorie et des pages à extraire, on demande confirmation puis on appelle la fonction
# pour écrire un fichier csv
def close_win(x,y,z):
    validation=tk.Tk()
    validation.title("Validation")
    validation.geometry("400x400")
    var=tk.IntVar()
    var.set(1)

    label=tk.Label(validation,text=f"Vous confirmez extraction de catégorie {x} entre pages : {y} et {z}")
    label.pack(pady=10)
    radio1=tk.Radiobutton(validation,text="oui",variable=var,value=1)
    radio2=tk.Radiobutton(validation,text="non",variable=var,value=2)
    last_one=tk.Button(validation,text="Valider",command=extraction_csv(x,y,z))

    radio1.pack(pady=10)
    radio2.pack(pady=10)
    last_one.pack(pady=10)

    validation.mainloop()

#quand l'utilisateur modifie la sélection de la catégorie, on met à jour nbre de pages correspondant
def mise_a_jour(*args):
    nbre_page=0
    global abc

    choix=var_1.get()
    if choix=="Tous":
        url_base="https://books.toscrape.com/index.html"
    elif choix in listecat :
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(listecat.index(choix))+"/index.html"
    else:
        pass  

    etape1 = requests.get(url_base)
    etape2 = BeautifulSoup(etape1.text,"html.parser")
    #trouver le nombre total de livres...
    trouve_strong=etape2.find_all("strong")

    strong_liste=[]
    #...pour en déduire le nombre total de pages (avec 20 livres par page)
    for i in trouve_strong:
        strong_liste.append(i.text)
    nbre_page=math.ceil(int(strong_liste[1])/20)

    abc=nbre_page
    label_var.set(f"Pour cette catégorie, il y a au total {abc} pages")
    

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
etik2.pack(pady=30)
var_3=tk.Entry(root, width=10)
var_3.insert(0,"10")
var_3.pack(pady=40)

label2=tk.Label(root,textvariable=label_var)
label2.pack(pady=10)

var_1.trace_add("write",mise_a_jour)
v1=var_1.get()

def check_ok():
    try :
        v2=int(var_2.get())
        v3=int(var_3.get())

        if v2>v3 or v3>abc :
            messagebox.showinfo("ERREUR","Nombre trop élévé ou incohérence")
        else:
            v1=var_1.get()
            v2=int(var_2.get())
            v3=int(var_3.get())
            close_win(v1,v2,v3)
    except ValueError:
            messagebox.showinfo("Erreur","Entrez uniquement des nombres")



valider=tk.Button(root,text="Valider",command=check_ok)
valider.pack(pady=10)



root.mainloop()
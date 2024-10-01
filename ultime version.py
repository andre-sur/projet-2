import tkinter as tk
import requests
import math
import os
import shutil
from bs4 import BeautifulSoup
from tkinter import messagebox

def update_selection (event) :

#Fonction pour récupérer le nombre de livres pour une catégorie
# et calculer (arrondi d'une division par 20) le nombre de pages concernées

#Il y a deux situations : tous les livres ("Books" ou "Tous") et une catégorie spécifique
#Ce qui entraine deux urls différents et un emplacement du nombre de livres différent
    emplacement=0
    choix=categories_menu.curselection()
    
    if categories_menu.get(choix[0])=="Tous" or categories_menu.get(choix[0])=="Books" :
        url_base="https://books.toscrape.com/index.html"
        emplacement=0
    else :
        url_base="https://books.toscrape.com/catalogue/category/books/"+categories_menu.get(choix[0]).lower().replace(" ","-")+"_"+str(choix[0])+"/index.html"
        emplacement=1

    #Je balaie l'url et trouve le contenu d'une balise "strong"
    #dont l'emplacement est variable (selon l'url) et qui contient la qtité de livres
    etape1 = requests.get(url_base)
    etape2 = BeautifulSoup(etape1.text,"html.parser")
    trouve_strong=etape2.find_all("strong")

    total_livre=trouve_strong[emplacement].text
    nbre_page=math.ceil(int(total_livre)/20)
    
    if choix:
        selected_index=choix[0]
        selected_item=categories_menu.get(selected_index)
        string_var.set (selected_item)
    
    label_var.set(f"Sélection en cours : {categories_menu.get(categories_menu.curselection()[0])} \n Total de {total_livre} livres, {nbre_page} pages")
    
    return(nbre_page)

def extraction_ciblee(categorie,first_page,last_page):
    #Fonction qui extrait les livres pour une catégorie et des pages données
    #...puis va les enregistrer dans un fichier CSV
    #Fonction appelée par le bouton correspondant dans fenêtre principale
   
    total_livres=nombre_livre(categorie)
    serie_select=balayage_des_livres(categorie,first_page,last_page,maxbook=total_livres)
    nom_du_fichier=categorie+"_page"+str(first_page)+"to"+str(last_page)+".csv"

    ecrire_fichier(nom_du_fichier,repertoire="Extractions ciblees",liste_finale=serie_select)

def extraire_toutes_categories ():
   
    #je fais une copie de la liste des catégories de laquelle je retire
    #la première catégorie deux fois ("Books" et "Tous" sont identiques)

    liste_sous_categories=liste_des_categories.copy()
    del liste_sous_categories[0]
    del liste_sous_categories[0]
    
    #Demande de confirmation à l'utilisateur
    decision=messagebox.askyesno("Confirmation","Voulez vous extraire tous les livres de chaque catégorie et les placer dans un répertoire ?")
    if decision:
        messagebox.showinfo("Ecriture","Cliquez OK.Patientez. C'est bientôt prêt.")
    # On boucle chaque élément de la liste de catégorie et on lui applique une extraction
        for categorie_en_cours in liste_sous_categories:
            nbre_livres=nombre_livre(categorie_en_cours)
            nbre_page=math.ceil(nbre_livres/20)
            liste_extraite=extraction_csv(categorie_en_cours,1,nbre_page,nbre_livres)
            
            ecrire_fichier(categorie_en_cours,"Par categories",liste_finale=liste_extraite)
    else : 
        messagebox.showinfo("Annulation","Aucune écriture.")

def nombre_livre(choix):
   
    if choix=="Tous":
        url_base="https://books.toscrape.com/index.html"
    elif choix in liste_des_categories :
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(liste_des_categories.index(choix))+"/index.html"
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

def check_validation():
    
    categorie_choisie=string_var.get()
    livres=nombre_livre(categorie_choisie)
    max=calcul_maxpage(categorie_choisie,"","w")

    try :
        frompage=int(from_page.get())
        untilpage=int(until_page.get())
        if frompage>untilpage :
           messagebox.showinfo("ERREUR","Incohérence dans les pages demandées")
           return
        elif untilpage>max :
            messagebox.showinfo("ERREUR","Cette catégorie a "+str(max)+" pages.")
            return

    except ValueError:
            messagebox.showinfo("Erreur","Erreur de saisie")

    validation=messagebox.askyesno("Confirmation","Vous confirmez l'extraction de la catégorie "+categorie_choisie+"? \nDans le fichier "+categorie_choisie+"_page"+str(frompage)+"to"+str(untilpage)+".csv \nDans le répertoire : Extractions ciblees")
    if validation :
        extraction_ciblee(categorie_choisie,frompage,untilpage)    
    else:
        messagebox.showinfo("ANNULATION","Opération annulée")

def creation_liste_categories():
    
    url = "https://books.toscrape.com/catalogue/page-1.html"
    contenu = requests.get(url)
    soupe = BeautifulSoup(contenu.text,"html.parser")

    #EXTRACTION DES CATEGORIES
    totale=soupe.find_all("ul",class_="nav nav-list")
    liste_des_categories=[]

    for i in totale:
        liste_des_categories=i.get_text(separator=",",strip=True).split(",")

    liste_des_categories.insert(0,"Tous")

    return(liste_des_categories)

def recupere_photos ():
    nbre_page=40 
    liens=[]
    tous=[]
    url_image=""
    if not os.path.exists("Images"):
        os.makedirs("Images")
    print("nombre de pasge début boucle extract"+str(nbre_page))
    decision=messagebox.askyesno("Confirmation","Voulez vous extraire toutes les images et les placer dans un répertoire unique ?")
    if decision:
        messagebox.showinfo("Ecriture","Patientez. C'est bientôt prêt.")
       
        for boucle in range (1,nbre_page):
       
            url="https://books.toscrape.com/catalogue/page-"+str(boucle)+".html"

            contenu = requests.get(url)
            soup=BeautifulSoup(contenu.text,"html.parser")
        
            tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

            print(url)  
            print(tous) 
       
            for livre in tous:   
                liens.append("https://books.toscrape.com/"+livre.find("img").attrs["src"][3:])
            
            for variable in range (0,len(liens)):
                url_image=liens[variable]
                print(url_image)
                response=requests.get(url_image,stream=True)
                if response.status_code==200:
                    with open (os.path.join("Images","image"+str(variable)+".jpg"),"wb") as file:
             #
                        shutil.copyfileobj(response.raw, file)
                
                else : 
                    print ("Impossible de télécharger")
    else : 
        messagebox.showinfo("Annulation","Aucune écriture.")
#Fonction pour créer un fichier csv formaté à partir des choix faits (catégorie, quelles pages extraire)
def extraction_csv(categorie,from_page,derniere_page,maxbook):

    nbre_livre=0
    listelivre=[]
    serie_totale=[]
    notation=["One","Two","Three","Four","Five"]
    prices=[]
    titres=[]
    dispo=[]
    rating=[]
    liens=[]

    for boucle in range (from_page,derniere_page+1):
        
        print("boucle " + str(boucle))
        print("CATEGORIE "+categorie)
      
        if from_page==1 and derniere_page==1:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/index.html"
        else:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/page-"+str(boucle)+".html"

        contenu = requests.get(url)
        soup = BeautifulSoup(contenu.text,"html.parser")
   
        livres_de_la_page=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
      
        for livre in livres_de_la_page:
             
            titres.append(livre.find("img").attrs["alt"])
            liens.append("https://books.toscrape.com/"+livre.find("img").attrs["src"][3:])
            prices.append(livre.find("p", class_="price_color").text[2:])
            dispo.append(livre.find("p", class_="instock availability").text.strip())
            nbre_livre=nbre_livre+1

            les_balises_p=livre.find_all("p")
        #On extrait la "note" des balises p : c'est la seconde de la liste donc [1]       
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
           
 #je compose une liste contenant les éléments pour chaque bouquin (format csv en colonnes avec virgule)
    for j in range(0,nbre_livre):
        print(j)
        serie_totale.append(titres[j]+","+prices[j]+","+dispo[j]+","+liens[j]+","+rating[j])


    return(serie_totale)

def Extraction_data_book(page):

    url=page
    response=requests.get(url)
    response.encoding="utf-8"
    livre=[]
    livre.append(url)

    if response.status_code==200:
        soupe=BeautifulSoup(response.text,"html.parser")

        livre.append(soupe.find("h1").text)

#RECHERCHE LA NOTATION
#RECHERCHE LA NOTATION
        les_balises_p=soupe.find_all("p")
        #On extrait la "note" des balises p : c'est la seconde de la liste donc [1]       
        for z in les_balises_p : 
            try : 
                z.get("class",[])[1]
                if z.get("class",[])[1] in ["One","Two","Three","Four","Five"]:
                    y=z.get("class",[])[1]
                    livre.append(y)
                    break
                else:
                    pass
                         
            except IndexError:
                pass
#RECHERCHE IMAGE
        lien_image=soupe.find("img").attrs["src"]
        print("AAAAAAAAAAA"+lien_image)
        livre.append(lien_image)

#RECHERCHE CATEGORIE AVEC BOUCLE
        div3=soupe.find("ul",class_="breadcrumb")
        li=div3.find_all("li")
        print("CATEGORIE   "+li[2].text.strip())
        livre.append(li[2].text.strip())
            
#RECHERCHE DESCRIPTION AVEC BOUCLE
        div=soupe.find("div",id="product_description",class_="sub-header")
        if div:
            p=div.find_next_sibling("p")
            if p:
                livre.append(p.text)
            else:
                print("pas de p dans cette div")
            
        else:
            print("pas de dic avec cet id")

#RECHERCHE LES ELEMENTS
        div2=soupe.find("table",class_="table table-striped")
        fragmentation=div2.find_all("td")
        for f in fragmentation:
            livre.append(f.text)
        livre[11]=livre[11].replace("In stock (","")
        livre[11]=livre[11].replace(" available)","")
        del livre[12]
        #print(livre)
        livre2='# '.join(livre)
        print("======================="+livre2[6])

    else:
        print("Erreur lors de la demande", response.status_code)
    
    return(livre2)

def balayage_des_livres(categorie,from_page,derniere_page,maxbook):
    nbre_livre=maxbook
    listelivre=[]
    serie_totale=[]

    outuve=""
    categorie="Fiction"
   

    for boucle in range (from_page,derniere_page+1):
        
        print("boucle " + str(boucle))
        print("CATEGORIE "+categorie)
      
        if from_page==1 and derniere_page==1:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/index.html"
        else:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/page-"+str(boucle)+".html"

        contenu = requests.get(url)
        soup = BeautifulSoup(contenu.text,"html.parser")
   
        livres_de_la_page=soup.find_all("article",class_="product_pod")
        print(livres_de_la_page)
        
        for livre in livres_de_la_page:       
       
            allthelinks=livre.find_all("div",class_="image_container")

            for liens in allthelinks:

                lienlivre="https://books.toscrape.com/catalogue/"+liens.find("a").attrs["href"][9:]
                print(lienlivre)


            
                listelivre.append(Extraction_data_book(lienlivre))
            
    return(listelivre)
           


def ecrire_fichier (nom_du_fichier,repertoire,liste_finale):  
    liste_finale=[element+"\n" for element in liste_finale] 
    liste_finale.insert(0,"url;titre;rating;image;categorie;description;upc;type;prix_ht;prix_ttc;prix;disponible \n")
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)                       
    with open(os.path.join(repertoire,nom_du_fichier),"w", encoding="utf-8") as fichier:
       
        fichier.writelines(liste_finale)
        
def calcul_maxpage(choix,index,mode):
    emplacement=0
    choix=string_var.get()
    
    if choix=="Tous":
        url_base="https://books.toscrape.com/index.html"
        emplacement=0
    elif choix in liste_des_categories :
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(liste_des_categories.index(choix))+"/index.html"
        emplacement=1
    else:
        url_base="https://books.toscrape.com/index.html" 

    etape1 = requests.get(url_base)
    etape2 = BeautifulSoup(etape1.text,"html.parser")
   
    trouve_strong=etape2.find_all("strong")

    total_livre=trouve_strong[emplacement].text
   
    nbre_page=math.ceil(int(total_livre)/20)
 
    label_var.set(f"Total de {total_livre} livres, {nbre_page} pages")
    
    return(nbre_page)

#PROGRAMME PRINCIPAL

#Fenêtre principale
root=tk.Tk()
root.title("Projet #1 - Extraction de données (scraping)")
root.geometry("500x500")
liste_des_categories=creation_liste_categories()
 
#Déclaration des variables
from_page=tk.StringVar(root)
until_page=tk.StringVar(root)
label_var=tk.StringVar()
string_var=tk.StringVar()

#Intitulé de la fenêtre et instructions utilisateur
en_tete=tk.Label(root,text="Extractor 2.0",font=("Arial",14),bg="white",fg="red")
en_tete.pack(pady=3)

first_line=tk.Label(root,text="Scrollez via l'ascenseur \n Cliquez pour sélectionner",font=("Arial",11),bg="white",fg="black")
first_line.pack(pady=1)

#Sous-fenêtre contenant les catégories pour sélection (avec ascenseur)
frame=tk.Frame(root)
frame.pack(pady=20)

scrollbar=tk.Scrollbar(frame,orient=tk.VERTICAL)
categories_menu=tk.Listbox(frame,yscrollcommand=scrollbar.set,height=6,selectmode=tk.SINGLE)
categories_menu.pack(side=tk.LEFT,fill=tk.BOTH)

scrollbar.config(command=categories_menu.yview)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

#Introduire une à une chaque categorie dans le menu
for item in liste_des_categories:
    categories_menu.insert(tk.END,item)

#Mettre à jour la sélection faite sur le menu est modifiant le texte
#à propos du nombre de pages, de titres pour la catégorie sélectionnée
categories_menu.bind('<<ListboxSelect>>',update_selection)

calcul_maxpage ("Tous","","w")

#Une étiquette avec un contenu variable et affiche
#nombre de pages et de livres pour la sélection en cours
information_courante_selection=tk.Label(root,textvariable=label_var)
information_courante_selection.pack(pady=3)

#Deux zones de texte à insérer pour les pages à sélectionner
#Avec une valeur par défaut de 1
texte_frompage=tk.Label(root,text="A partir de la page :",font=("Arial",10,"bold"))
texte_frompage.pack(pady=2)
from_page=tk.Entry(root, width=10)
from_page.insert(0,"1")
from_page.pack(pady=2)

text_untilpage=tk.Label(root,text="Jusqu'à la page :",font=("Arial",10,"bold"))
text_untilpage.pack(pady=2)
until_page=tk.Entry(root, width=10)
until_page.insert(0,"1")
until_page.pack(pady=2)

#Un bouton pour extraire la sélection en cours càd
#Les pages sélectionnées pour la catégorie sélectionnée
valider=tk.Button(root,text="Extraire la sélection en cours",command=check_validation)
valider.pack(pady=2)

#Un bouton pour faire l'extraction de la totalité des catégories
#...lesquelles seront rangées dans un répertoire à part, un fichier csv par catégorie
extraire_toutes_categories=tk.Button(root,text="Extraire toutes les catégories",command=extraire_toutes_categories)
extraire_toutes_categories.pack(pady=2)

#Un bouton pour faire l'extraction de toutes les photos
#...lesquelles seront rangées dans un répertoire à part, un ficher jpg par photo
extraire_photos=tk.Button(root,text="Extraire toutes les photos",command=recupere_photos)
extraire_photos.pack(pady=2)

root.mainloop()
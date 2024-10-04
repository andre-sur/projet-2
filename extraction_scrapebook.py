import tkinter as tk
import time
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
#Ce qui entraine deux urls différents et un emplacement où trouver le nombre de livres différent
    emplacement=0
    # la variable "choix" est la catégorie sur laquelle a cliqué l'utilisateur
    # c'est pour celle ci qu'on va afficher nombre de pages et de livres 

    choix=categories_menu.curselection()
    
    if categories_menu.get(choix[0])=="Tous" or categories_menu.get(choix[0])=="Books" :
        url_base="https://books.toscrape.com/index.html"
        emplacement=0
    else :
        url_base="https://books.toscrape.com/catalogue/category/books/"+categories_menu.get(choix[0]).lower().replace(" ","-")+"_"+str(choix[0])+"/index.html"
        emplacement=1

    #Je balaie l'url et trouve le contenu d'une balise "strong"
    #dont l'emplacement est variable (selon l'url) et qui contient la qtité de livres
    donnees_url = requests.get(url_base)
    parsing_url = BeautifulSoup(donnees_url.text,"html.parser")
    balises_strong=parsing_url.find_all("strong")

    total_livre=balises_strong[emplacement].text
    nbre_page=math.ceil(int(total_livre)/20)
    
    if choix:
        selected_index=choix[0]
        selected_item=categories_menu.get(selected_index)
        string_var.set (selected_item)
#Je change le contenu de l'étiquette sur le menu principal qui annonce nbre de pages et livres pour catégorie
    label_var.set(f"Sélection en cours : {categories_menu.get(categories_menu.curselection()[0])} \n Total de {total_livre} livres, {nbre_page} pages")
    
    return(nbre_page)

def extraction_ciblee(categorie,first_page,last_page):
    #Fonction qui extrait les livres pour une catégorie et des pages données (sélection menu)
    #...puis va les enregistrer dans un fichier CSV
    #Fonction appelée par le bouton correspondant dans menu principal
   
    total_livres=nombre_livre(categorie)
    serie_select=parsing_des_livres(categorie,first_page,last_page,maxbook=total_livres)
    nom_du_fichier=categorie+"_page"+str(first_page)+"to"+str(last_page)+".csv"

    ecrire_fichier(nom_du_fichier,repertoire="Extractions ciblees",liste_finale=serie_select)

    messagebox.showinfo("Fin des opérations","Toutes les images ont été enregistrées.")
    root.destroy()


def extraire_toutes_categories ():
   
    #je fais une copie de la liste des catégories de laquelle je retire
    #la première catégorie deux fois ("Books" et "Tous" sont identiques)
    #ceci afin d'avoir une liste des categories uniquement (pour le traitement)

    liste_sous_categories=liste_des_categories.copy()
    del liste_sous_categories[0]
    del liste_sous_categories[0]
    
    #Demande de confirmation à l'utilisateur
    decision=messagebox.askyesno("Confirmation","Voulez vous extraire tous les livres de chaque catégorie et les placer dans un répertoire ?")
    if decision:
        messagebox.showinfo("Ecriture","Cliquez OK.Patientez. C'est bientôt prêt.")
    # On itère pour chaque élément de la liste de catégorie et on extrait les données de livre pour chacune
        for categorie_en_cours in liste_sous_categories:
            nbre_livres=nombre_livre(categorie_en_cours)
            nbre_page=math.ceil(nbre_livres/20)
    #Appel à la fonction qui extrait toutes les données livre pour la catégorie
    #...et met le tout dans une liste
            liste_extraite=parsing_des_livres(categorie_en_cours,1,nbre_page,nbre_livres)
    #Appel de la fonction qui enregistre la liste en format csv dans un répertoire
            ecrire_fichier(categorie_en_cours,"Par categories",liste_finale=liste_extraite)
    else : 
        messagebox.showinfo("Annulation","Aucune écriture.")
    
def nombre_livre(categorie_concernee):
   #Va chercher l'info à propos du nombre de livre pour une catégorie donnée
    if categorie_concernee=="Tous":
        url_base="https://books.toscrape.com/index.html"
    elif categorie_concernee in liste_des_categories :
        url_base="https://books.toscrape.com/catalogue/category/books/"+categorie_concernee.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie_concernee))+"/index.html"
    else:
        url_base="https://books.toscrape.com/index.html" 

    donnees_url = requests.get(url_base)
    parsing_url = BeautifulSoup(donnees_url.text,"html.parser")
    # On va chercher dans les balises "strong" et récupérer la deuxième (indice 1)
    # Elle contient le nombre de livres pour la catégorie
    balises_strong=parsing_url.find_all("strong")

    strong_liste=[]
    for i in balises_strong:
        strong_liste.append(i.text)
    total_livres=int(strong_liste[1])
    return(total_livres)

def ok_validation():
    #Fonction enclenchée quand user demande extraction pour catégorie et pages déterminées
    categorie_choisie=string_var.get()
    livres=nombre_livre(categorie_choisie)
    max=calcul_maxpage(categorie_choisie,"","w")

# On vérifie que les données concernant les pages sont correctes/cohérentes
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
# On demande confirmation 
    validation=messagebox.askyesno("Confirmation","Vous confirmez l'extraction de la catégorie "+categorie_choisie+"? \nDans le fichier "+categorie_choisie+"_page"+str(frompage)+"to"+str(untilpage)+".csv \nDans le répertoire : Extractions ciblees")
    if validation :
        extraction_ciblee(categorie_choisie,frompage,untilpage)    
    else:
        messagebox.showinfo("ANNULATION","Opération annulée")

def creation_liste_categories():
#Fonction qui va chercher dans le menu la liste des catégories de livre (page index)
    url = "https://books.toscrape.com/catalogue/page-1.html"
    contenu = requests.get(url)
    page_principale = BeautifulSoup(contenu.text,"html.parser")

#EXTRACTION DU MENU
    recherche_menu=page_principale.find_all("ul",class_="nav nav-list")
    liste_des_categories=[]
#EXTRACTION DE CHAQUE ELEMENT DU MENU POUR EN FAIRE UNE LISTE
    for categories in recherche_menu:
        liste_des_categories=categories.get_text(separator=",",strip=True).split(",")

    liste_des_categories.insert(0,"Tous")

    return(liste_des_categories)

def recupere_photos ():
    #Fonction qui récupère toutes les photos/images (appelée par bouton)
    #...à partir des pages principales (pas les livres en détail)
    #...les photos sont plus petites et rangés dans un répertoire "Images"
    nbre_page=calcul_maxpage("https://books.toscrape.com/index.html",index="",mode="") 
    liens=[]
    tous=[]
    toutes_photos=[]
    url_image=""
    if not os.path.exists("Images"):
        os.makedirs("Images")
    
    decision=messagebox.askyesno("Confirmation","Voulez vous extraire toutes les images et les placer dans un répertoire unique ?")
    if decision:
        messagebox.showinfo("Ecriture","Patientez. C'est bientôt prêt.")
        root.destroy()

        for boucle in range (1,nbre_page):
       
            url="https://books.toscrape.com/catalogue/page-"+str(boucle)+".html"
            time.sleep(1)
            contenu = requests.get(url)
            soup=BeautifulSoup(contenu.text,"html.parser")
        
            tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

       
            for livre in tous:   
                liens.append("https://books.toscrape.com/"+livre.find("img").attrs["src"][3:])
            
            for variable in range (0,len(liens)):
                url_image=liens[variable]
            #ajout d'un délai d'attente pour éviter les soucis d'éjection du site
                time.sleep(1)
                response=requests.get(url_image,stream=True)
                if response.status_code==200:
                    with open (os.path.join("Images","image"+str(variable)+".jpg"),"wb") as file:
             #
                        shutil.copyfileobj(response.raw, file)
                
                else : 
                    pass
        messagebox.showinfo("Fin des opérations","Toutes les images ont été enregistrées.")
        root.destroy()
    else : 
        messagebox.showinfo("Annulation","Aucune écriture.")    
    messagebox.showinfo("Fin des opérations","Le téléchargement des images est terminé.")

def recupere_photos_hi_def ():
     #Fonction qui récupère toutes les photos/images (appelée par bouton)
    #...à partir de chaque livre 
    #...les photos sont plus GRANDES (hi def) et rangés dans un répertoire "Images haute def"
    nbre_page=calcul_maxpage("https://books.toscrape.com/index.html",index="",mode="") 
    liens=[]
    lien_livre=""
    tous=[]
    toutes_photos=[]
    url_image=""
    if not os.path.exists("Images haute def"):
        os.makedirs("Images haute def")
    print("nombre de pasge début boucle extract"+str(nbre_page))
    decision=messagebox.askyesno("Confirmation","Voulez vous extraire toutes les images et les placer dans un répertoire unique ?")
    if decision:
        messagebox.showinfo("Ecriture","Patientez. C'est bientôt prêt.")

        for boucle in range (1,nbre_page):
       
            url="https://books.toscrape.com/catalogue/page-"+str(boucle)+".html"

            contenu = requests.get(url)
            soup=BeautifulSoup(contenu.text,"html.parser")
                
            tous=soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
       
            for livre in tous:
                allthelinks=livre.find_all("div",class_="image_container")

                for liens in allthelinks:

                    lien_livre="https://books.toscrape.com/catalogue/"+liens.find("a").attrs["href"]

                #lien_livre="https://books.toscrape.com/"+livre.find("img").attrs["src"][3:]
                    balayage = requests.get(lien_livre)
                    balayage2=BeautifulSoup(balayage.text,"html.parser")
                    lien_image="https://books.toscrape.com/"+balayage2.find("img").attrs["src"][6:]
                    print(lien_image)
                #liens.append(lien_image)
                messagebox.showinfo("Fin des opérations","Toutes les images ont été enregistrées.")
                root.destroy()
                    
def Extraction_data_book(page):
#Fonction pour extraire toutes les données d'un livre
#...en ayant comme paramètre sa page url
#renvoie une liste avec un livre par élément de liste 
#choix du séparateur # car beaucoup de ; et , notamment dans la rubrique "description"
    url=page
    response=requests.get(url)
    response.encoding="utf-8"
    livre=[]
    livre.append(url)

    if response.status_code==200:
        soupe=BeautifulSoup(response.text,"html.parser")
        livre.append(soupe.find("h1").text)

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
        lien_image="https://books.toscrape.com/"+soupe.find("img").attrs["src"][6:]    
        livre.append(lien_image)

#RECHERCHE CATEGORIE AVEC BOUCLE
        div3=soupe.find("ul",class_="breadcrumb")
        li=div3.find_all("li")
        #récupérer deuxième balise "li" et retirer l'inutile autour 
        #c'est la catégorie du livre et on l'ajoute
        livre.append(li[2].text.strip())
            
#RECHERCHE DESCRIPTION AVEC BOUCLE
#...et mettre une description vide si pas trouvée (ça arrive)
        div=soupe.find("div",id="product_description",class_="sub-header")
        if div:
            p=div.find_next_sibling("p")
            if p:
                livre.append(p.text)
            else:
                livre.append("")            
        else:
            livre.append("")

#RECHERCHE LES ELEMENTS
        div2=soupe.find("table",class_="table table-striped")
        fragmentation=div2.find_all("td")
        for f in fragmentation:
            livre.append(f.text)
        livre[11]=livre[11].replace("In stock (","")
        livre[11]=livre[11].replace(" available)","")
        #Effacer une donnée extraite inutile (indice 12)
        del livre[12]
        #Mettre le séparateur # entre les données et former une chaine de caractère
        livre2='# '.join(livre)

    else:
        print("Erreur lors de la demande", response.status_code)
    
    return(livre2)

def parsing_des_livres(categorie,from_page,derniere_page,maxbook):

    #Fonction CENTRALE
    #Balaie des pages spécifiées d'une catégorie donnée
    #...et extrait pour chaque livre toutes ses données (via une autre fonction : Extraction_data_book)
    nbre_livre=maxbook
    listelivre=[]
    #serie_totale=[]

    for boucle in range (from_page,derniere_page+1):
      
        if from_page==1 and derniere_page==1:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/index.html"
        else:
            url="https://books.toscrape.com/catalogue/category/books/"+categorie.lower().replace(" ","-")+"_"+str(liste_des_categories.index(categorie))+"/page-"+str(boucle)+".html"

        contenu = requests.get(url)
        soup = BeautifulSoup(contenu.text,"html.parser")
   
        livres_de_la_page=soup.find_all("article",class_="product_pod")
        #print(livres_de_la_page)
        
        for livre in livres_de_la_page:       
       
            allthelinks=livre.find_all("div",class_="image_container")
    #Une boucle pour récupérer les données pour chaque livre de cette page
    #...et l'ajouter à listelivre
            for liens in allthelinks:

                lienlivre="https://books.toscrape.com/catalogue/"+liens.find("a").attrs["href"][9:]
             
                listelivre.append(Extraction_data_book(lienlivre))
    #on renvoie la liste de tous les livres pour cette catégorie     
    return(listelivre)

def ecrire_fichier (nom_du_fichier,repertoire,liste_finale):  
    #Enregistre un fichier texte avec tel nom, tel répertoire et une liste
    #...dans un format csv avec saut à la ligne entre chaque élément

    liste_finale=[element+"\n" for element in liste_finale] 
    liste_finale.insert(0,"url#titre#rating#image#categorie#description#upc#type#prix_ht#prix_ttc#prix#disponible \n")
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)                       
    with open(os.path.join(repertoire,nom_du_fichier),"w", encoding="utf-8") as fichier:
       
        fichier.writelines(liste_finale)
        
def calcul_maxpage(choix,index,mode):
    #Fonction de calcul du nombre de page pour une catégorie
    #...à partir du nombre de livre divisé par 20 arrondi au supérieur
    #Renvoie le nombre de page
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
valider=tk.Button(root,text="Extraire la sélection en cours",command=ok_validation)
valider.pack(pady=2)

#Un bouton pour faire l'extraction de la totalité des catégories
#...lesquelles seront rangées dans un répertoire à part, un fichier csv par catégorie
extraire_toutes_categories=tk.Button(root,text="Extraire toutes les catégories",command=extraire_toutes_categories)
extraire_toutes_categories.pack(pady=2)

#Un bouton pour faire l'extraction de toutes les photos
#...lesquelles seront rangées dans un répertoire à part, un ficher jpg par photo
extraire_photos=tk.Button(root,text="Extraire toutes les photos",command=recupere_photos)
extraire_photos.pack(pady=2)

extraire_photos_hi_def=tk.Button(root,text="Extraire toutes les photos HAUTE DEFINITION",command=recupere_photos_hi_def)
extraire_photos_hi_def.pack(pady=2)

root.mainloop()
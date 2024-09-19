import requests
from bs4 import BeautifulSoup


url = "https://books.toscrape.com/catalogue/page-1.html"

contenu = requests.get(url)
    
soupe = BeautifulSoup(contenu.text,"html.parser")
#EXTRACTION DES CATEGORIES
menu=soupe.find_all("ul",class_="nav nav-list")
        #print (tous)
#print (menu)

for i in menu:
    listecat=i.get_text(separator=",",strip=True).split(",")

def combienpageurl (u):
    contenu = requests.get(u)
    nbre_page=contenu.find("li",class_="current").text.strip()[10:12]
    return(nbre_page)


def fenetre_page(u):
    root=tk.Tk()
    root.title("QUELLE PAGE")
    root.geometry("300x200")

    label2=tk.Label(root,text="Choisissez quelle page")
    label2.pack(pady=10)
    numeropage=ttk.Combobox(root,values=list(range(1,int(combienpageurl(u)))))

    numeropage.pack(pady=5)

    root.mainloop()

    return()

def quelle_url(selection):
    if selection=="Tous":
        url_base="https://books.toscrape.com/index.html"
    else :
        #url_cible="https://books.toscrape.com/catalogue/category/books/"+selection.lower().replace(" ","-")+"_"+str(listecat.index(selection))+"/page-"+num_page+".html"
        #url_base="https://books.toscrape.com/index.html"
        url_base="https://books.toscrape.com/catalogue/category/books/"+selection.lower().replace(" ","-")+"_"+str(listecat.index(selection))+"/index.html"

    return(url_base)

#EXTRACTION DES CATEGORIES
menu=soupe.find_all("ul",class_="nav nav-list")
        #print (tous)
#print (menu)

for i in menu:
    listecat=i.get_text(separator=",",strip=True).split(",")

#listecat[8]="INTR#US"
print (listecat)
#print (len(listecat))
listecat.insert(0,"Tous")

def quelle_categorie (max):
    for i in range(max):
        print (i)
       # print (str(i)+">"+listecat[i])

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog


   # messagebox.showinfo("Sélection",f"Vous avez sélectionné : {selection}"+" - "+str(listecat.index(selection))+"\n"+url_cible+"\n Et la page numéro")
fenetre_page(url_base)
root=tk.Tk()
root.title("Choix de la catégorie à extraire")
root.geometry("300x200")

#label instruction et menu déroulant
label=tk.Label(root,text="Choisissez la catégorie")
label.pack(pady=10)

combobox=ttk.Combobox(root,values=listecat)

combobox.pack(pady=5)
combobox.current(1)
selection=combobox.get()


bouton_valider=tk.Button(root,text="Valider",command=fenetre_page(url_base))
bouton_valider.pack(pady=10)

root.mainloop()

if selection=="Tous":
        url_base="https://books.toscrape.com/index.html"
else :
        #url_cible="https://books.toscrape.com/catalogue/category/books/"+selection.lower().replace(" ","-")+"_"+str(listecat.index(selection))+"/page-"+num_page+".html"
        #url_base="https://books.toscrape.com/index.html"
        url_base="https://books.toscrape.com/catalogue/category/books/"+selection.lower().replace(" ","-")+"_"+str(listecat.index(selection))+"/index.html"
        print(listecat.index("Music"))
        print(selection)

fenetre_page(url_base)

"""
#champ de saisie du numéro de page
numero_page=tk.Label(root,text="Entrez un numéro de page de 1 à 50:")
numero_page.pack(pady=5)

numero=tk.Entry(root,width=10)
numero.pack(pady=5)

try:
    n=int(numero.get())
except ValueError:
    messagebox.showinfo("Erreur","Entrez un nombre")

verif_nombre(n,1,50)

#Bouton de validation
bouton_valider=tk.Button(root,text="Valider")
bouton_valider.pack(pady=10)
"""


root.mainloop()
                                 

#double menu interdépendant - la base
import tkinter as tk
import requests
import math
from bs4 import BeautifulSoup
from tkinter import messagebox
abc=33
def sortie_interface():
    messagebox.showinfo("Sortie interface")

def close_win():
    validation=tk.Tk()
    validation.title("Validation")
    validation.geometry("400x400")
    var=tk.IntVar()
    var.set(1)

    label=tk.Label(validation,text=f"Vous confirmez que vous voulez une extraction")
    label.pack(pady=10)
    radio1=tk.Radiobutton(validation,text="oui",variable=var,value=1)
    radio2=tk.Radiobutton(validation,text="non",variable=var,value=2)
    last_one=tk.Button(validation,text="Valider",command=sortie_interface)

    radio1.pack(pady=10)
    radio2.pack(pady=10)
    last_one.pack(pady=10)


    validation.mainloop()

def mise_a_jour(*args):
    #menu_1["menu"].delete(0,"end")
    nbre_page=0
    #nouvelle_options=list(range(1,50))
    global abc

    choix=var_1.get()
    if choix=="Tous":
        
        url_base="https://books.toscrape.com/index.html"

        etape1 = requests.get(url_base)
        etape2 = BeautifulSoup(etape1.text,"html.parser")
        trouve_strong=etape2.find_all("strong")

        strong_liste=[]
        for i in trouve_strong:
            strong_liste.append(i.text)
        #liste=i.get_text(separator=",",strip=True).split(",")
        nbre_page=math.ceil(int(strong_liste[0])/20)
        abc=nbre_page
        label_var.set(f"Pour cette catégorie, il y a au total {abc} pages")

        #nouvelle_options=list(range(1,nbre_page)) 
        #nouvelle_options.insert(0,"Toutes") 
        #nouvelle_options=["ou","joi","kol"]
    elif choix in listecat :
        #url_cible="https://books.toscrape.com/catalogue/category/books/"+selection.lower().replace(" ","-")+"_"+str(listecat.index(selection))+"/page-"+num_page+".html"
        #url_base="https://books.toscrape.com/index.html"
        
        url_base="https://books.toscrape.com/catalogue/category/books/"+choix.lower().replace(" ","-")+"_"+str(listecat.index(choix))+"/index.html"
        """
        etape1 = requests.get(url_base)
        etape2 = BeautifulSoup(etape1.text,"html.parser")
        nbre_page=etape2.find("li",class_="current").text.strip()[10:12]
        """
        etape1 = requests.get(url_base)
        etape2 = BeautifulSoup(etape1.text,"html.parser")
        trouve_strong=etape2.find_all("strong")

        strong_liste=[]
        for i in trouve_strong:
            strong_liste.append(i.text)
        #liste=i.get_text(separator=",",strip=True).split(",")
        nbre_page=math.ceil(int(strong_liste[1])/20)

        abc=nbre_page
        label_var.set(f"Pour cette catégorie, il y a au total {abc} pages")
        #nouvelle_options=list(range(1,nbre_page)) 
        #nouvelle_options.insert(0,"Toutes") 
        #nouvelle_options=["aa","bb","cc"] 
    
        
    else:
        nouvelle_options=["kjkjkj","lklklk","oioiezd"]                                                                                                                                           
                     
   # for option in nouvelle_options:
    #    menu_2["menu"].add_command(label=option,command=tk._setit(var_2,option))

    return(nbre_page)

root=tk.Tk()
root.title("Menus dépendants")
root.geometry("300x400")

# ooooooooooooooooooooooooooooooooooooooooooooooooooo CATEGORIES

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

def check_ok():
    try :
        v2=int(var_2.get())
        v3=int(var_3.get())

        if v2>v3 or v3>abc :
            messagebox.showinfo("NON","HORS CHAMPS")
        else:
            close_win()
    except ValueError:
            messagebox.showinfo("PAS CHIFFRE","METTRE CHIFFRE")



valider=tk.Button(root,text="Valider",command=check_ok)
valider.pack(pady=10)



root.mainloop()
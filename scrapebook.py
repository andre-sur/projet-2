import requests
from bs4 import BeautifulSoup

def extraction_csv (categorie, a,b):

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
        
        url="https://books.toscrape.com/catalogue/category/books/"+categorie+"_10/page-"+str(x)+".html"
        print(url)
        contenu = requests.get(url)
            
        soupe = BeautifulSoup(contenu.text,"html.parser")
            #categorie= categorie_0.text[0:soupe.title.text.index("|")]
                
        tous=soupe.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        print (tous)
            #categorie = tous.find("title").string.text[0:soupe.title.text.index("|")]

        for livre in tous:
                        #titres=livre.get_text(separator=",",strip=True).split(",")
                    #categories.append(categorie)
                titres.append(livre.find("img").attrs["alt"])
                liens.append(livre.find("a").attrs["href"])
                prices.append(livre.find("p", class_="price_color").text[2:])
                dispo.append(livre.find("p", class_="instock availability").text.strip())
        #Récupérer et ajouter le rating
                touslesps=livre.find_all("p")
                        #rating.append(livre.find("p class",True,"star-rating.*"))
                        #for a in touslesas:
                            #if a.get("class",[])[0]=="star-rating":
                for z in touslesps : 
                            #print(a)
                            #b=a.find("p").attrs["class"]
                            #print(b)
                    try : 
                        z.get("class",[])[1]
                        if z.get("class",[])[1] in notation:
                            y=z.get("class",[])[1]
                            rating.append(y)
                        else:
                            pass
                                
                    except IndexError:
                        pass
                        
                        

                        
                            #print(a)
                            #print((a.get("class",[])[0]))
                        
        #je compose une liste contenant les éléments pour chaque bouquin
        for j in range(1+(x-1)*20,len(tous)+(x-1)*20):
                    
            serie_totale.append(titres[j]+","+prices[j]+","+dispo[j]+","+liens[j]+","+rating[j])
    serie_totale.insert(0,"titre,prix,disponible,lien,note")                    



    #je transforme une liste en ligne avec les éléments séparés par des virgules (autre méthode à tester)

    def mise_en_ligne (a=list):

        ligne=a[0]
        for i in range(len(a)-1):
            ligne=ligne+","+a[i+1]
                    
        return ligne


            #j'écris un fichier csv avec pour chaque ligne titre et prix séparés par virgule et un header titre,prix
    with open("extraction.csv","w") as f:
        for j in range(0,len(serie_totale)):
            f.write (f"{serie_totale[j]}\n")
            f.close


    print(serie_totale)
        

    #print(ligne)
    #print (prices)
    #print (titres)
    #print (prices)
extraction_csv("fiction",1,4)
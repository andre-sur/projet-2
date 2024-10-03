import requests
from bs4 import BeautifulSoup

def Extraction_data_book(page):

    url=page
    response=requests.get(url)
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

        print(livre)
        livre2=', '.join(livre)
        print("======================="+livre2)

    else:
        print("Erreur lors de la demande", response.status_code)
    
    return(livre2)


nbre_livre=0
listelivre=[]
serie_totale=[]
from_page=1
derniere_page=1
outuve=""
categorie="Fiction"

for boucle in range (from_page,derniere_page+1):
        
    print("boucle " + str(boucle))
    print("CATEGORIE "+categorie)
      
    url="https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
        
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
            


print(listelivre)
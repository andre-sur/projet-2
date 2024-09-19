import requests
import math
from bs4 import BeautifulSoup


liste=[]
url_base="https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
 
etape1 = requests.get(url_base)
etape2 = BeautifulSoup(etape1.text,"html.parser")
trouve_strong=etape2.find_all("strong")

for i in trouve_strong:
    liste.append(i.text)
    #liste=i.get_text(separator=",",strip=True).split(",")
print(liste[0])
#nbre_page=math.ceil(int(liste[0])/20)

#print(nbre_page)  
entree=input("entrez une liste de chiffres séparés par des virgules")
liste=entree.split(",")

print (liste)
print("addition")
somme=0
for i in liste:
    j=int(i)
    somme+=j
print(f"total {somme}")
print(f"moyenne {somme/len(liste)}")
moyenne=somme/len(liste)

print("multiplication")
produit=1
for i in liste:
    j=int(i)
    produit=produit*j
print(f"total produit {produit}")

print ("nombre entier supérieur à moyenne")
increme = 0
for y in liste:
    if int(y) >= moyenne:
        increme+=1
print(f"nombre sup à moyenne {increme}")

print("nombre pairs")
pair=0
for z in liste:
    if int(z)%2==0:
        pair+=1
print (f"nombre de pairs {pair}")

from operations import multiplication

test=multiplication(8,7)
print(test)

def salairemensu(a):
    salaire=a/12
    return (salaire)
def salairehebdo(b):
    hebdo=b/4
    return(hebdo)
def horairefric (c,dol):
    frichor=int(dol)/int(c)

    return(frichor)


frican=input("combien tu touches par an")
heuretravail=input("combien d'heures travaillées par semaine")
z=salairemensu(int(frican))
h=salairehebdo(z)
i=horairefric(heuretravail,h)
print (f"salaire mensu {z}")
print (f"salaire hebdo {h}")
print (f"fric par heure {i}")
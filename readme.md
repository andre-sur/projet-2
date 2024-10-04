

# Mode d’emploi utilisateur  
   
## Extraction de pages définies pour une catégorie ciblée

L’utilisateur clique sur la catégorie. S’affichent alors le nombre de livres, et le nombre de page (de site) pour la-dite catégorie.  
L’utilisateur introduit la première et dernière page dans les cases correspondantes.  
Enfin, il appuie sur Valider, se voit proposer une confirmation.  
Le fichier est sauvegardé sur le répertoire “Extractions ciblees” et le nom est une combinaison categorie+page+(x)+a+(y).csv. Ceci afin d'avoir une indication du contenu dans le titre. Par exemple : "Fiction_page_1_a_2.csv"

Notez bien : le séparateur retenu est "#". En effet, il y a du texte dans la rubrique "description", lequel contient des ";" et des ",". Il faut donc un séparateur spécifique pour éviter les ambiguités.

Voici les rubriques :
url#titre#rating#image#categorie#description#upc#type#prix_ht#prix_ttc#prix#disponible 

## Extraction de toutes les pages, rangées par catégorie, dans un répertoire spécifique

L’utilisateur clique sur le bouton. Il confirme son choix.  
S’il n’existe pas, un répertoire “Par categories” est créé et contient la totalité des extractions, chaque catégorie étant appelé par son nom, en format csv.
Attention, l'extraction prend du temps, au minimum 30 minutes.
Un message s'affiche lorsqu'elle est terminée.

## Extraction de toutes les images, rangées dans un répertoire unique

L’utilisateur clique sur le bouton, confirme son choix.  
S’il n’existe pas déjà, un répertoire “Images” est créé et contient toutes les images issues du site. Les images récupérées sont celles en petit format (et basse définition) qui se trouve sur la page générale de présentation des livres, pour une catégorie donnée.

## Extraction de toutes les images, en haute définition, rangées dans un répertoire unique
L’utilisateur clique sur le bouton, confirme son choix.  
S’il n’existe pas déjà, un répertoire “Images haute def” est créé et contient toutes les images issues du site, plus spécifiquement de la présentation de chaque livre, dans laquelle se trouve une image grand format avec une meilleure définition.

Attention, les opérations d'extraction de tous les livres et images prennent au minimum 20 à 30 minutes. Un message s'affiche lorsque l'opération est terminée.

# Notes à propos du programme (fonctions, architecture)

## Extraction de pages ciblées pour une catégorie  
- cliquer sur une catégorie enclenche la fonction update_selection qui met à jour le nombre de pages et titres pour ladite sélection (sur le menu principal)  
- cliquer sur valider déclenche la fonction "ok_validation" qui vérifie que les numéros de page entrés sont cohérents et retourne un message d’erreur si ça n’est pas le cas.   
- si on clique sur valider et que tout est cohérent, on a un message demandant confirmation de la validation demandée. Si on confirme, la fonction "extraction_ciblee" est alors lancée et extrait les données puis les enregistre sur le répertoire “Extractions ciblees”   

## Extraction de toutes les pages
- lorsqu’on clique sur “Extraire toutes les pages”, la fonction "extraire_toute_categorie" est lancée. Elle fait un boucle sur toutes les pages, puis une recherche pour chaque livre apparaissant sur la page. 
Via l'url de la page du livre, elle récupère les données en détails (fonction: extraction data book). Et met le résultat dans une liste.

## Récupérer toutes les images (petit format)
   Lorsqu’on clique sur le bouton, la fonction "recuperer_images" est lancée et enregistre pour chaque page toutes les images dans un répertoire. Les images sont récupérées sur les pages principales, avec une boucle simple et un parsing qui enregistre les images.

## Récupérer toutes les images (haute définition)
   Lorsqu’on clique sur le bouton, la fonction "recuperer_images_hi_def" est lancée et enregistre pour chaque page toutes les images dans un répertoire. 
   Les images sont récupérées dans la présentation détaillée de chaque livre, en allant sur l'url de chaque livre qu'on récupère sur la page principale. 
     
## Fonctions spécifiques  
   nombre_livre : extrait en haut de page le nombre de livres pour la catégorie  
   creation_liste_categorie : extrait toutes les catégories dans le menu de la main page   
   calcul_maxpage : calcul le nombre total de pages d’une sélection  
   ecrire_fichier : selon ses paramètres (nom de fichier, répertoire, liste), enregistre une liste contenant des livres dans un fichier csv
   Extraction_data_book : récupère les éléments pour un livre spécifique sur la page url le concernant (et les ajoute à une liste)

	


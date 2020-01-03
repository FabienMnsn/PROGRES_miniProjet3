+--------------------+
| 		README		 |
+--------------------+


+--------------------+
| TABLE DES MATIERES |
+--------------------+


1) INFORMATIONS GENERALES

2) DESCRIPTION DETAILEE DES ROUTES BOTTLE (dans l'ordre du sujet)

3) CONCLUSION & AVIS




+------------------------+
| Informations générales |
+------------------------+


1)________________________________________________________________________________________________________
Nous avons choisi de créer une route bottle par defaut (http://localhost:8080/) qui est un menu principal.
Ce menu affiche plusieurs liens (href) pointant vers les différentes parties de l'API.
On retrouve les liens suivants :

- [Rechercher Auteur] 				qui redirige vers /auteur/qui
- [Rechercher Conference]			qui redirige vers /Conference/Laquelle
- [Graphe publication Lip6]			qui redirige vers /LIP6
- [Graphe publication 2 auteurs]	qui redirige vers /LIP6/auteurs

Les trois premiers liens sont directement issus du sujet ils repondents aux questions 1, 9 et 11.
Le dernier lien (/LIP6/auteurs) est une fonctionnalité en plus qui n'est pas demandée dans le sujet.
Pour plus d'informations sur la fonction, cherchez la section dédiée à cette fonction.


2)_________________________________________________________
Toutes les fonctions qui font le gros du travail à savoir :
- télécharger et traiter un fichier xml
- chercher les publications
- chercher les conférences
- chercher les coautheurs
- récupérer le rang Core 
se trouvent dans le fichier 'utils_xml.py'.
Le programme principal bottle se trouve dans le fichier 'mini_projet.py'.



+-----------------------------------------+
| Description détaillée des routes bottle |
+-----------------------------------------+

_____________________
ROUTE 1 : /auteur/qui

Cette route affiche une page html en utilisant une template page.tpl basique.
La page affiche un formulaire de saisie demande de rentrer le Nom et le Prénom d'un auteur.
La validation ce fait par un bouton.

La page affiche aussi 2 liens. Le premier est un retour vers le menu principal et le second redirige vers la route /Conference/Laquelle.
Cette route bottle gère les erreurs suivantes:
- Une saisie vide affiche une page html d'erreur "Saisie vide" avec une indication d'aide et un lien de retour à la saisie.

- Si le nom n'existe pas sur dblp ou qu'il est mal orthographié on retourne une page html disant "impossible de récupérer les informations de cette personne". Une indication d'aide et un lien de retour à la saisie sont aussi affiché sur la page d'erreur.

- S'il existe un homonyme ayant le même nom, on affiche une page d'erreur affichant "il existe plusieurs auteurs ayants le même nom", une indication d'aide et un lien de retour vers la saisie.



________________________
ROUTE 2 : /auteur/<name>

Cette route affiche une page html contenant un tableau récapitulatif de l'auteur avec le nombre d'articles publiés, le nombre de conférences et le nombre de co-auteurs.
Quand on clique sur chercher, la fonction va automatiquement télécharger le fichier xml correspondant à l'auteur. Ce fichier xml sera la base pour une grande majorité des fonctionnalités de l'API.
On retrouve aussi des liens vers les differentes parties de l'API qui concernent l'auteur.
On ne peut pas par exemple naviguer au graphe du lip6 via la page de l'auteur, il faut retourner au menu principal pour acceder a la route /LIP6 (ou la saisir directement dans la barre d'addresse).



__________________________________________
ROUTE 3 : /auteur/Journals/synthese/<name>

Cette route affiche un tableau ou chaque colonne est un rang Core (A*, A, B, C et Unranked).
En haut du tableau (première ligne), on retrouve le nombre de publication total de la colonne.
Dans chaque colonne on retrouve le nom du journal, l'année de publication et le nombre de publications dans ce journal.
On retrouve des liens de navigations vers le menu principal, vers la page de l'auteur et vers la page de synthèse des conférences.
Il arrive que des publications se retrouvent dans la catégorie "Unranked" alors qu'elle ont un rang sur le site core. cela est du au fait que les noms des journaux ne sont pas exactement les mêmes sur le site dblp et sur le site Core. Il peut y avoir des abréviations d'un mot qui fausse la recherche sur le site Core.



_________________________________
ROUTE 4 : /auteur/Journals/<name>

Cette route affiche une page html basée sur la template html basique (page.tpl) contenant un table détaillant toutes les publications d'un auteur.
On retrouve 4 colonnes qui sont : le nom de l'article, la liste des auteurs, le nom du journal et l'année de publication.
On retrouve aussi des liens vers les autre partie de l'API : un lien vers le menu principal, un lien vers la page de l'auteur (qui sert de mini menu principal) et un lien vers la page détaillant les conférences de l'auteur.
Cette fonction parcours le fichier xml de l'auteur et recupère tous les articles publiés.



_____________________________________________
ROUTE 5 : /auteur/Conferences/synthese/<name>

Cette route fait exactement la même chose que la route 3, elle présente une page html et un tableau des rangs Core.
Cette route peut prendre un peu de temps à s'afficher car la recherche du nom de la conférence sur le site Core peut donner un tableau de résultats très grand que l'on doit parcourir et tester tous les noms de conférences pour savoir si c'est la bonne.



___________________________________
ROUTE 6 : /auteur/Conference/<name>

Cette route fait exactement la même chose que la route 4.
Cette route est très rapide à s'afficher car on ne fait que parcourir le fichier source xml.
On retrouve les mêmes liens de navigation que ceux de la route 4.



____________________________________________
ROUTE 7 : /auteur/Conferences/Voyages/<name>

Cette route affiche une page html avec le nom de l'auteur et le nombre de lieux qui on été résoluts par geopy (par exemple 31/31 indique qu'il y a 31 lieux qui sont épinglés sur la carte sur les 31 qui sont présents dans le fichier de l'auteur).
On retrouve aussi une aide disant de zoomer si des conférence ont eu lieu au même endroit. Pour éviter se problème de marqueur au même endroit, si un marqueur est déja placé a cet endroit, on place le marqueur au même endroit en ajoutant un random dans les coordonnées gps (~0.005 en longitude) pour éviter que les marqueur soit les uns sur les autres.
On retrouve aussi des liens de navigation vers le menu principal et la page de l'auteur.
Cette route peut prendre beaucoup de temps à s'afficher à cauise du nombre de conférences a placer sur la carte, et du status de geopy.
pour résoudre les problèmes de time out de geopy, on a créé une fonction qui fait un appel récursif et s'endort si geopy retourne une exception de time out. 



__________________________________
ROUTE 8 : /auteur/coauthors:<name>

Cette route affiche une page html contenant un tableau avec une seule colonne avec un co-auteur par ligne.
Le titre du tableau affiche le nombre totalk de co-auteurs.
Cette route est très rapide en temps d'execution car on ne fait que parcourir le fichier xml source.
Au-dessus du tableau on retouve des liens pour naviguer vers le menu principal et la page de l'auteur.



______________________________
Route 9 : /Conference/Laquelle

Cette route affiche une page html avec un formulaire de saisie d'un acronyme de conférence similaire.
La page html est similaire à celle de saisie d'un auteur sauf qu'elle n'a qu'un seul champ de saisie.
Cette page propose aussi des lien de navigation vers le menu principal et vers la page de saisie d'un auteur (/auteur/qui).
Un bouton 'Chercher' permet de valider la saisie et de lancer la recherche.



____________________________
ROUTE 10 : /Conference/Lieux

Cette route affiche en titre le nom de la conférence (l'acronyme) avec un indicateur du nombre d'épingles placées avec geopy et une carte du monde avec des épingles. On retrouve aussi des liens de navigation vers le menu principal et vers la saisie d'un acronyme d'une conférence.
Cette route peut prendre un peut de temps a charger si il y beaucoup d'épingles a placer car il y a un sleep() dans l'appel a geopy pour gérer le cas du TimeOut.



________________
ROUTE 11 : /LIP6

Cette route est une route statique qui affiche un graphe des publications de tous les membres permanents du lip6.
Chaque membre est représenté par un noeud gris et une publication entre deuw membres est repésentée par un trait reliant les noeuds.

Nous avons rencontrés beaucoups de problèmes pour programmer cette route principalement à cause de la bibliothèque SageMath qui n'est pas très bien documentée et plutôt complexe à installer.
Nous avons donc utilisé une autre bibliothèque 'Networkx' qui permet de faire des graphes du même type que ceux de SageMath mais qui est utilisée par un grand nombre de personnes et possède une documentation bien fournie.
Cette route génère un graphe en objets networkx puis grâce à pyplot, l'enregistre au format png. On affiche ensuite le fichier générer sur la page. Chaque appel à la route /LIP6 regénère le graphe. La disposition des noeuds est aléatoire.
Pour générer le graphe nous avons utilisé un fichier XML contenant toutes les équipes du LIP6 et dans chaque équipe on retrouve tous les membres permanents.
Nous avons écrit se fichier XML avec un code de script python.



___________________________
ROUTE BONUS : /LIP6/auteurs

Cette route est une route bonus. Nous avons décidé d'ajouter cette route car elle nous semble pertinente.
Cette route affiche une page html avec un formulaire de saisie qui demande de saisir deux noms d'auteurs.
Elle fait le lien avec la route /LIP6/Graphe qui est une route statique.



__________________________
ROUTE BONUS : /LIP6/Graphe

Cette route affiche, comme la route /LIP6 un graphe Networkx rendu au format PNG.
Le graphe généré représente les deux auteurs par deux gros noeuds de couleur différente. Les membres du LIP6 qui on écrit avec un auteur qui a été saisie sont représenté par un noeud plus petit de la même couleur que l'auteur. Un trait entre deux noeud représente une relation de co-auteur.
Tous les autres membres permanents du LIP6 sont représentés par des petits noeuds gris.





+------------------------+
| 	Conclusion et avis   |
+------------------------+


Les problèmes rencontrés:

- Télécharger un fichier xml nous a posé des problèmes car ElementTreeXML crash à chaque code de caractères spéciaux comme par exemple '&123;'. On a donc du trouver un moyen de remplacer automatiquement les caractères spéciaux dans les fichiers xml par leur caractères en utf-8 (car l'encodage sur dblp n'est pas le bon c'est de l'iso 8856)

- La partie graphe a été complexe, on a perdu beaucoup de temps à essayer d'installer la bibliothèque correctement et à générer un rendu propre. Nous avons, au final, opté pour la bibliothèque NetworkX.

- Le sujet du projet n'est pas cohérent par certain moments, par exemple les urls ne sont jamais les mêmes une fois c'est en français une autre fois c'est en anglais. Nous avons opté dans la majorité des cas par le français. Il y a juste /auteurs/coauthors qui est en anglais.


En conclusion c'est un projet très intérressant à réaliser mais qui nécessite selon nous une amélioration du sujet, que les questions soit plus clairement expliquées.


			


+------------------------------------------+
| FABIEN MANSON		& 	  ALEXANDRE MAZARS |
+------------------------------------------+
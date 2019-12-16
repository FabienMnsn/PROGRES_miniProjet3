import xml.etree.ElementTree as ET


"""
recherche dans l'extrait du fichier dblp.xml
"""

#_____________________________________________________________________________________________________
					#Fonction qui repond à la spec de la question 2 du projet
#_____________________________________________________________________________________________________
def find_publication(author_name_to_find, tree_root):
	res = {"articles":0, "journaux":0, "conferences":0, "co-auteurs":0}
	for child in root:
		authors = child.findall('author')
		for author in authors:
			if(author.text == author_name_to_find):
				res["co-auteurs"] += len(authors)-1
				if(child.tag == "article"):
					title = child.find("title")
					if("Conference" in str(title.text)):
						res["conferences"] += 1
					else:
						res["articles"] += 1
				elif(child.tag == "journal"):
					res["journaux"] += 1
	return res
#_____________________________________________________________________________________________________



#_____________________________________________________________________________________________________
					#Fonction qui repond à la spec de la question 3 du projet
#_____________________________________________________________________________________________________
def tableau_publication(author_name_to_find, tree_root):
	tableau_publication = []
	for child in root:
		authors = child.findall('author')
		for author in authors:
			if(author.text == author_name_to_find):
				journal = child.find('journal')
				annee = child.find('year')
				if(journal != None and annee != None):
					tableau_publication.append([journal.text, annee.text])
	return tableau_publication
#_____________________________________________________________________________________________________


#_____________________________________________________________________________________________________
					#Fonction qui repond à la spec de la question 4 du projet
#_____________________________________________________________________________________________________
def liste_publication(author_name_to_find, tree_root):
	tableau_publication = []
	for child in root:
		liste = liste_auteurs(child)
		if(author_name_to_find in liste):
			liste.remove(author_name_to_find)
			title = child.find('title')
			journal = child.find('journal')
			annee = child.find('year')
			if(title != None and journal != None and annee != None):
				tableau_publication.append([title.text, liste, journal.text, annee.text])
	return tableau_publication
#_____________________________________________________________________________________________________


#------------------------------------------------------------------
#							Utilitaires
#------------------------------------------------------------------
def liste_auteurs(tree_element):
	l = []
	for child in tree_element:
		if(child.tag == 'author'):
			l.append(str(child.text))
	return l

#------------------------------------------------------------------



if __name__ == '__main__':

	##############################################
	#           	   MAIN TREE 				 #
	##############################################
	tree = ET.parse('XML/PARSED_extract_dblp.xml')
	root = tree.getroot()
	##############################################


	#trouver le nombre de publication (articles + journaux + conferences + co-auteurs)
	print("Résultats pour Frank Manola :", find_publication("Frank Manola", root))
	print("Résultats pour Paul Kocher  :", find_publication("Paul Kocher", root))


	#afficher un tableau des publications (journaux + date)
	print("\nTableau des publications de Frank Manola : ")
	for i in tableau_publication("Frank Manola", root):
		print(i)
	print("\nTableau des publications de Paul Kocher : ")
	for i in tableau_publication("Paul Kocher", root):
		print(i)

	#afficher le tableau détaillé des publications
	print("\nTableau des publications détaillé de Frank Manola : ")
	for i in liste_publication("Frank Manola", root):
		print(i)
	print("\nTableau des publications détaillé de Paul Kocher : ")
	for i in liste_publication("Paul Kocher", root):
		print(i)
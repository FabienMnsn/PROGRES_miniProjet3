import xml.etree.ElementTree as ET


"""
recherche dans l'extrait du fichier dblp.xml
"""

#_____________________________________________________________________________________________________
					#Fonction qui repond à la spec de la question 2 du projet
#_____________________________________________________________________________________________________
def find_publication(file_path):
	tree = ET.parse(file_path)
	root = tree.getroot()
	res = {"journaux":0, "conferences":0, "co-auteurs":0}
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'article'):
					res["journaux"] += 1
				elif(grandchild.tag == 'inproceedings'):
					res["conferences"] += 1
		elif(child.tag == 'coauthors'):
			for author in child:
				res["co-auteurs"] += 1

	return res
#_____________________________________________________________________________________________________



#_____________________________________________________________________________________________________
					#Fonction qui repond à la spec de la question 3 du projet
#_____________________________________________________________________________________________________
def tableau_publication(file_path):
	tree = ET.parse(file_path)
	root = tree.getroot()
	tableau_publication = []
	publication = []
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'article'):
					for article_data in grandchild:
						if(article_data.tag == "journal"):
							#acronyme ou titre => le mieux c'est titre selon nous
							#j_acronyme = to_acronyme(article_data.text)
							publication.append(article_data.text)
						if(article_data.tag == "year"):
							annee = article_data.text
							publication.append(annee)
					tableau_publication.append(publication)
					publication = []
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

def to_acronyme(journal_name):
	name_splited = journal_name.split(' ')
	acronyme = ""
	for word in name_splited:
		acronyme += ""+word[0].upper()
	return acronyme


def liste_vers_html(liste, legende):
	"""
	Retourne une table html faite a partir d'une double liste python (liste de liste)

	@param
	liste : la double liste
	legende : string decrivant la legende sseparee par des ';'
	"""
	legende_split = legende.split(';')
	table_head = "<table style='width:100%'>\n<caption>Table des publications</caption>\n"
	table_content = ""
	table_bottom = "</table>"
	if(len(legende_split)) != len(liste[0]):
		return -1
	if(type(liste) == list and type(liste[0]) == list):
		table_content += "<tr>\n"
		for lgd in legende_split:
			table_content += "<th>"+lgd+"</th>\n"
		table_content += "</tr>"
		for objet in liste:
			table_content += "<tr>\n"
			for elem in objet:
				table_content += "<td>"+elem+"</td>\n"
			table_content += "</tr>\n"
		return table_head+table_content+table_bottom
	else:
		print("liste pas correcte")
	#for elem in liste:

"""
style a incerer pour la table

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: left;
}
"""
def liste_auteurs(tree_element):
	l = []
	for child in tree_element:
		if(child.tag == 'author'):
			l.append(str(child.text))
	return l

#------------------------------------------------------------------



if __name__ == '__main__':

	"""
	author_name = input("Saisir un nom d'auteur: ")
	file_path = "Auteurs/"+author_name+".xml"
	print(find_publication(file_path))
	print(tableau_publication(file_path))
	"""
	print(liste_vers_html(tableau_publication("Auteurs/Pierre Sens.xml"), "Année de publication; Nom du journal"))
	"""
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
	"""
import xml.etree.ElementTree as ET


def publication_stat(file_path):
	"""
	Retourne un dictionnaire contenant les statistiques de publication d'un auteur : journaux, conferences, co-auteurs
	
	@param
	file_path : string, chemin d'accès du fichier XML de l'auteur ex:"Auteurs/Nom Prénom.xml"
	"""
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


def liste_resume_publication(file_path):
	"""
	Retourne une liste resumee de toutes les publications d'un auteur [publication, annee]

	@param
	file_path : chemin du fichier xml source, par ex: 'Auteurs/Olivier Fourmaux.xml'
	"""
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


def liste_detail_publication(file_path):
	"""
	Retourne une liste complete de toutes les publications d'un auteur avec pour chaque publication : 
	le titre, la liste des auteurs, le nom du journal et l'annee de publication

	@param
	file_path : chemin du fichier xml source, par ex: 'Auteurs/Olivier Fourmaux.xml'
	"""
	tree = ET.parse(file_path)
	root = tree.getroot()
	tableau_publication = []
	publication = []
	titre = ""
	auteur_liste = ""
	journal_name = ""
	annee = ""
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'article'):
					for article_data in grandchild:
						if(article_data.tag == "journal"):
							#acronyme ou titre => le mieux c'est titre selon nous
							#j_acronyme = to_acronyme(article_data.text)
							journal_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
						if(article_data.tag == "title"):
							titre = article_data.text
						if(article_data.tag == "author"):
							auteur_liste += article_data.text+", "
					publication.append(titre)
					publication.append(auteur_liste[:-2])
					publication.append(journal_name)
					publication.append(annee)
					tableau_publication.append(publication)
					publication = []
					titre = ""
					annee = ""
					auteur_liste = ""
					journal_name = ""
	return tableau_publication


def liste_resume_conference(file_path):
	"""
	Retourne une liste resumee de toutes les conferences d'un auteur [conference, annee]

	@param
	file_path : chemin du fichier xml source, par ex: 'Auteurs/Olivier Fourmaux.xml'
	"""
	tree = ET.parse(file_path)
	root = tree.getroot()
	tableau_conferences = []
	conference = []
	annee = ""
	conference_name = ""
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'inproceedings'):
					for article_data in grandchild:
						if(article_data.tag == "booktitle"):
							#acronyme ou titre => le mieux c'est titre selon nous
							#c_acronyme = to_acronyme(article_data.text)
							conference_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
					conference.append(conference_name)
					conference.append(annee)
					tableau_conferences.append(conference)
					conference = []
					conference_name = ""
					annee = ""
	return tableau_conferences


def liste_detail_conference(file_path):
	"""
	Retourne une liste complete de toutes les conferences d'un auteur avec pour chaque conference : 
	le titre, la liste des auteurs, le nom de la conference et la date 

	@param
	file_path : chemin du fichier xml source, par ex: 'Auteurs/Olivier Fourmaux.xml'
	"""
	tree = ET.parse(file_path)
	root = tree.getroot()
	tableau_conferences = []
	conf = []
	titre = ""
	auteur_liste = ""
	conference_name = ""
	annee = ""
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'inproceedings'):
					for article_data in grandchild:
						if(article_data.tag == "booktitle"):
							#acronyme ou titre => le mieux c'est titre selon nous
							#c_acronyme = to_acronyme(article_data.text)
							conference_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
						if(article_data.tag == "title"):
							titre = article_data.text
						if(article_data.tag == "author"):
							auteur_liste += article_data.text+", "
					conf.append(titre)
					conf.append(auteur_liste[:-2])
					conf.append(conference_name)
					conf.append(annee)
					tableau_conferences.append(conf)
					conf = []
					titre = ""
					annee = ""
					auteur_liste = ""
					conference_name = ""
	return tableau_conferences

#------------------------------------------------------------------
#							Utilitaires
#------------------------------------------------------------------

def to_acronyme(journal_name):
	"""
	Retourne l'acronyme c-a-d les premieres lettres de chaque mot de journal_name

	@param
	journal_name : une string representant le nom du journal
	"""
	name_splited = journal_name.split(' ')
	acronyme = ""
	for word in name_splited:
		acronyme += ""+word[0].upper()
	return acronyme


def liste_vers_html(liste, legende_colonne, legende_table):
	"""
	Retourne une table html faite a partir d'une double liste python (liste de liste)

	@param
	liste : la double liste
	legende_colonne : string decrivant la legende de chaque colonne separee par des ';' ex: "Conference;Auteurs;Annee"
	legende_table : legende de la table : <caption>legende_table</caption>
	"""
	legende_split = legende_colonne.split(';')
	table_head = "<table style='width:100%'>\n<caption>"+legende_table+"</caption>\n"
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
		print("liste incorrecte")
		return -1

#------------------------------------------------------------------
#------------------------------------------------------------------


if __name__ == '__main__':

	"""
	author_name = input("Saisir un nom d'auteur: ")
	file_path = "Auteurs/"+author_name+".xml"
	print(find_publication(file_path))
	print(tableau_publication(file_path))
	"""
	#name = input("Saisir un nom d'auteur pour afficher la liste detaillee des publications :")
	#print(liste_vers_html(liste_resume_conference("Auteurs/"+name+".xml"), "Titre;Auteurs;Journal;Année", "Table détailéé des publications"))
	#print(liste_vers_html(tableau_publication("Auteurs/Pierre Sens.xml"), "Année de publication; Nom du journal"))
	#print(liste_vers_html(liste_detail_conference("Auteurs/Olivier Fourmaux.xml"), "Conférence;Année", "Liste des conférences"))
	print(liste_vers_html(liste_detail_conference("Auteurs/Vincent Guigue.xml"), "titre;auteurs;nom du book;annee", "liste des conferences"))
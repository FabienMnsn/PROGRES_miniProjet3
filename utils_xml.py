import requests
import re
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

#############################################################################################################
#																											#
# 	Ceci est un fichier regroupant les fonctions qui sont nécéssaires au fonctionnement de notre API 		#
#																											#
#############################################################################################################



#------------------------------------------------------------------------------------------------------------
# 							Fonctions permettant de télécharger un fichier XML 
#------------------------------------------------------------------------------------------------------------
def create_dico_html(caracter_table_file_path):
	"""
	Cree un ditionnaire des codes html correspondants au caracteres speciaux html
	(Il servira a créer la requete http pour télécharger le fichier XML)

	@param
	caracter_table_file_path : "/Doxuments/table_html.txt"
	"""
	dico = {}
	table = open(caracter_table_file_path, "r", encoding='utf-8')
	line = table.readline()
	while(line != ""):
		stri = line.split('|')
		dico[stri[0]] = stri[1][1:-2]
		line = table.readline()
	table.close()
	return dico


def request_author_file_builder(author_name, table_path):
	"""
	Retourne une url de requete donnant accès au fichier XML correspondant au nom de l'auteur en parametre
	
	@param
	author_name : string représentant le nom et le prénom d'un auteur  ex:"Prenom Nom"
	table_path : chemin d'accès du fichier source permeetant de créer le dictionnaire des caratères spéciaux
	"""
	dico = create_dico_html(table_path)
	splited_name = list(author_name)
	splited_changed = []
	for char in splited_name:
		if(char in dico):
			splited_changed.append('='+dico[char]+'=')
		else:
			splited_changed.append(char)
	author_name_changed = "".join(splited_changed)
	author_name_split = author_name_changed.split(' ')
	#on remplace le trait d'union par un = pour générer la requete
	first_name_maybe_composed = author_name_split[1].replace('-', '=')
	name_maybe_composed = author_name_split[0].replace('-', '=')
	name_first_letter_cut = author_name_split[1][0].lower()
	request = "https://dblp.uni-trier.de/pers/xx/"+name_first_letter_cut+"/"+first_name_maybe_composed+":"+name_maybe_composed+".xml"
	return request


def download_file(author_name, download_path, table_path):
	"""
	Telecharge et parse un fichier xml correspondant au nom de l'auteur passe en parametre.

	@param
	author_name : string représentant le nom et le prénom d'un auteur  ex:"Prenom Nom"
	download_path : chemin d'accès du repertoire ou le fichier sera téléchargé ex:"XML/downloads/"
	table_path : string, chemin d'acces de la table html
	"""
	requested = requests.get(request_author_file_builder(author_name, table_path))
	#print("---->DOWNLOAD :", request_author_file_builder(author_name, table_path))
	file_name = download_path+"_"+author_name+".xml"
	if(requested.status_code == 200):
		with open(file_name, 'wb') as local_file:
			for chunk in requested.iter_content(chunk_size=128):
				local_file.write(chunk)
		local_file.close()
		parse_file(file_name, download_path+author_name+".xml", "table_iso.txt")
		os.remove(file_name)
	else:
		print("error", requested.status_code)
	return requested.status_code






#------------------------------------------------------------------------------------------------------------
# 			Fonctions permettant de transformer les caractères spéciaux présents dans le fichier XML 
#------------------------------------------------------------------------------------------------------------
def create_dico_iso(table_file_path):
    """
    Fonction qui fabrique un dictionnaire à partir d'un fichier de codes iso de carateres spéciaux.
    chaque clé est un code de type &uml; et la valeur associée est un caractere spécial

    @parma
    table_file_path : chemin d'accès du fichier source permettant de créer le dictionnaire (par simple lecture du fichier)
    """
    #print("----Création du dictionnaire de référence")
    file = open(table_file_path, 'r', encoding='utf-8')
    line = file.readline()
    dict = {}
    while(line != ""):
        stri = line.split('|')
        dict[stri[1][:-1]] = stri[0]
        line = file.readline()
    file.close()
    return dict


def split_char_code(string):
    """
    Fonction qui split une chaine de caracteres en une liste de carateres.
    le critere de split est de la forme &auml; (c'est un code iso pour représenter les caracteres spéciaux)

    @param
    string : ligne d'un fichier à découper
    """
    res = []
    start_index = 0
    end_index = 0
    for i in range(len(string)):
        if(string[i] == "&"):
            end_index = i
            res.append(string[start_index:end_index])
            start_index = i
        if(string[i] == ';'):
            end_index = i+1
            res.append(string[start_index:end_index])
            start_index = i+1
        else:
            end_index = i
    res.append(string[start_index:end_index+1])
    return extend_split_char_code(res)


def extend_split_char_code(string):
    """
    Fonction qui split un tableau de chaine de caracteres en un autre tableau de carateres en separant les '&' qui se trouvent seuls.

    @param
    string : tableau de streing représentant une ligne du fichier
    """
    res = []
    for elem in string:
        if(len(elem) == 0):
            continue
        elif('&' in elem and elem[0] == '&' and elem[-1] != ';'):
            res.append(elem[0])
            res.append(elem[1:])
        elif(elem[0] != '&' and elem[-1] == ';'):
            #changé le 17/12/19
            res.append(elem[:-1])
        else:
            res.append(elem)
    return res


def replace_char(splited_string, dictionnaire):
    """
    Remplace le code iso dans splited _string par le caractere corespondant.
    S'il n'existe pas, on remplace par le caractere vide.
    (Car de toute façon le code iso fait crasher le parser Elementtree...)
    Et retourne la ligne assemblée (joined)

    @param
    splited_string : tableau de string qui represente une ligne complete du fichier
    dictionnaire : dictionnaire des codes iso
    """
    res = []
    for elem in splited_string:
        #si c'est un '&' seul on le remplace par 'and'
        if(elem == '&' and len(elem) == 1):
            res.append("and")
        #si c'est un code de caractere special, on le cherche deans le dico et on le remplace
        elif('&' in elem and ';' in elem):
            if(elem in dictionnaire):
                #elem = dico[elem[:-1]]
                res.append(dictionnaire[elem])
            else:
                elem = ""
                res.append(elem)
        else:
            res.append(elem)
    return ''.join(res)


def cut_end(ligne):
    """
    Enleve le dernier caractere de la ligne si et seulement si c'est un retour a la ligne
    """
    if(ligne[-1] == '\n'):
        return ligne[:-1]
    else:
        return ligne


def xml_formater(input_file, output_file, dictionnaire_code):
    """
    Reformatage du fichier pour pouvoir le parser correctement.
    WIP => il est possible que cette fonction ne serve a rien si
    on trouve la solution pour que le parser XML dans python ne crash pas des qu'il rencontre un '&' ou un '#'...
    
	@param
	input_file : chemin d'acces du fichier source
	output_file : chemin de sortie du fichier généré
	dictionnaire_code : dictionnaire associant à chaque code iso le caratère correspondant
    """
    #recuperation du dictionnaire des codes iso
    dictio = dictionnaire_code
    xml = open(input_file, 'r')
    #fichier de sortie
    new_xml = open(output_file, 'w', encoding='utf-8')
    new_xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")

    #print("--------Ouverture de :", input_file, ", création de :", output_file)
    for line in xml:
        #on enleve le retour chariot a la fin de la ligne s'il y en a un
        line_ = cut_end(line)
        #si c'est la ligne de definition de la version, on ne la traite pas 
        #car on la remlace par la bonne valeur au debut de la fonction xml_formater
        if("version" in line_):
            continue
        elif("<ee>" in line_ and "</ee>" in line_):
        	continue
        else:
            #contains_special_char = re.search(r"&", line_)
            #line2_ = line_.replace("<-->", "")
            line2_ = line_
            if("<-->" in line_):
            	print(line_)
            contains_special_char = ('&' in line2_)
            #if(contains_special_char != None and len(contains_special_char[0]) > 0):
            if(contains_special_char):
                splited_line = split_char_code(line2_)
                new_line = replace_char(splited_line, dictio)
                new_xml.write(new_line+"\n")
                #print(line_)
                #print(new_line)
            else:
                new_xml.write(line2_+"\n")
    new_xml.close()
    xml.close()
    #print("--------Fermeture des fichiers", input_file, ", ", output_file)


def parse_file(input_file_path, output_file_path, table_correspondance):
	"""
	Fonction qui appelle les differentes autres fontions nécéssaire pour transformer tous les codes iso dans le fichier input_file_path
	
	@param
	input_file_path : string du chemin d'accès du fichier source à traiter
	output_file_path : string du chemin d'accès du fichier de destination (fichier resultant du traitement)
	table_correspondance : string du chemin d'accès du fichier source permettant de créer le dictionnaire d'association des codes iso
	"""
	dico = create_dico_iso(table_correspondance)
	xml_formater(input_file_path, output_file_path, dico)






#------------------------------------------------------------------------------------------------------------
# 						Fonctions permettant de parser un fichier XML avec ElementTree
#------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------
#			Fonction concernant les journaux
#-------------------------------------------------------
def liste_lip6(file_path):
	"""
	Retourne la liste de tous les membres permanents du lip6 en inversant nom et prenom

	@param
	file_path : string, chemin d'acces du fichier xml contenant tous les membres permanents du lip6
	"""
	res = []
	tree = ET.parse(file_path)
	root = tree.getroot()
	for child in root:
		for membre in child:
			name = membre.text
			name_splited = name.split(' ')
			nom = '-'.join(name_splited[:-1])
			#print(nom)
			res.append(name_splited[-1]+" "+nom)
	return res


def get_coauteurs(file_path):
	"""
	Retourne une liste de co-auteurs de l'auteur passe en parametres

	@param
	file_path : string, chemin d'acce du fichier de l'auteur
	"""
	res = []
	tree = ET.parse(file_path)
	root = tree.getroot()
	for child in root:
		if(child.tag == 'coauthors'):
			for grandchild in child:
				for elem in grandchild:
					name = re.sub(r'[0-9]*', '', elem.text)
					res.append(name)
	return res


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
	file_path : chemin du fichier XML source, par ex: 'Auteurs/Olivier Fourmaux.xml'
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
							publication.append(article_data.text)
						if(article_data.tag == "year"):
							annee = article_data.text
							publication.append(annee)
					tableau_publication.append(publication)
					publication = []
	return tableau_publication


def get_rank_journal(journal_name):
	"""
	Retourne le classement core (A*, A, B ou C) ou -1 s'il n'y a pas d'informations

	@param
	journal_name : string, nom du journal extrait du fichier xml de l'auteur
	"""
	if(journal_name == ""):
		return ""
	journal_names_concat = journal_name.replace(' ', '+')
	journal_names_concat2 = journal_names_concat.replace('.','')
	journal_name_clean = journal_name.replace('.', '')
	url = "http://portal.core.edu.au/jnl-ranks/?search="+journal_names_concat2+"&by=all&source=all"
	#proxy = {"https":"https://proxy.ufr-info-p6.jussieu.fr:3128"}
	r = requests.get(url) # , proxies=proxy)
	soup = BeautifulSoup(r.content, "html.parser")
	res = soup.find_all('tr')
	#print(res)
	for elem in res:
		if(elem == res[0]):
			continue
		else:
			resultat = search_line_journal(elem, journal_name_clean)
			if(resultat != ""):
				return resultat
	return "Unranked"
	

def search_line_journal(table_row, journal_name):
	"""
	Cherche si la ligne correspond au nom de journal et  retourne le rang du journal ou une chaine vide si pas d'infos
	
	@param
	table_row : BeautifulSoup Element, ligne de table html a parcourir
	journal_name : string, nom du journal trouvé dans le fichier XML
	"""
	line = table_row.find_all('td')
	name = clean_string(line[0].text)
	rank = clean_string(line[2].text)
	name_splited = name.split(' ')
	journal_splited = journal_name.split(' ')
	i_j = 0
	i_n = 0
	found = False
	while (not(found)):		
		if(name_splited[i_n] == "of" or name_splited[i_n] == "and" or name_splited[i_n] == "on"):
			#print("---skiped", name_splited[i_n])
			i_n += 1
			continue
		if(name_splited[i_n] == "The" or name_splited[i_n] == "the"):
			#print("---skiped THE", name_splited[i_n])
			i_n += 1
			continue
		if(journal_splited[i_j] in name_splited[i_n]):
			#print("---"+journal_splited[i_j]+" in "+name_splited[i_n])
			i_n +=1
			i_j +=1
		else:
			return ""
		if(i_n == len(name_splited) or i_j == len(journal_splited)):
			found = True
			return rank
	return ""


def clean_string(string):
	"""
	Retourne une chaine de caracteres sans les espaces en trop a cause de beautifulsoup
	"""
	if(len(string) <= 0):
		return ""
	else:
		string_2 = string.replace('\n', '')
		string_splited = string_2.split(' ')
		res = ""
		for i in string_splited:
			if(len(i) > 0):
				res += i+' '
		return res[:-1]


def display_rank_journal(journal_name):
	"""
	Simple fonction de test permettant de tester rapidement la fonction get_rank()

	@param
	journal_name : string, nom du journal
	"""
	print("DISPLAY_RANK | Journal :",journal_name,", rank :",get_rank_journal(journal_name))



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
							journal_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
						if(article_data.tag == "title"):
							titre = article_data.text
						if(article_data.tag == "author"):
							name = re.sub(r'[0-9]*', '', article_data.text)
							auteur_liste += name+", "
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


#-------------------------------------------------------
#			Fonctions concernant les conferences
#-------------------------------------------------------
def liste_resume_conference(file_path):
	"""
	Retourne une liste resumee de toutes les conferences d'un auteur [conference, annee, url]

	@param
	file_path : chemin du fichier xml source, par ex: 'Auteurs/Olivier Fourmaux.xml'
	"""
	tree = ET.parse(file_path)
	root = tree.getroot()
	tableau_conferences = []
	conference = []
	url = ""
	annee = ""
	conference_name = ""
	for child in root:
		if(child.tag == 'r'):
			for grandchild in child:
				if(grandchild.tag == 'inproceedings'):
					for article_data in grandchild:
						if(article_data.tag == "booktitle"):
							conference_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
						if(article_data.tag == "url"):
							url = article_data.text
					conference.append(conference_name)
					conference.append(annee)
					conference.append(url)
					tableau_conferences.append(conference)
					conference = []
					#conference_name = ""
					#annee = ""
					#url = ""
	return tableau_conferences


def get_rank_conference(conference_name):
	"""
	Retourne le classement core (A*, A, B ou C) ou -1 s'il n'y a pas d'informations

	@param
	conference_name : string, nom du journal extrait du fichier xml de l'auteur
	"""
	if(conference_name == ""):
		return ""
	conference_name_concat = conference_name.replace(' ', '+')
	url = "http://portal.core.edu.au/conf-ranks/?search="+conference_name_concat+"&by=all&source=all"
	#print(url)
	#proxy = {"https":"https://proxy.ufr-info-p6.jussieu.fr:3128"}
	r = requests.get(url) # , proxies=proxy)
	soup = BeautifulSoup(r.content, "html.parser")
	res = soup.find_all('tr')
	for elem in res:
		if(elem == res[0]):
			continue
		else:
			resultat = search_line_conference(elem, conference_name)
			if(resultat != ""):
				return resultat
	return "Unranked"


def search_line_conference(table_row, conference_name):
	"""
	Cherche si la ligne correspond au nom de la conference et retourne le rang du journal ou une chaine vide si pas d'infos
	
	@param
	table_row : BeautifulSoup Element, ligne de table html a parcourir
	conference_name : string, nom du journal trouvé dans le fichier XML
	"""
	line = table_row.find_all('td')
	name = clean_string(line[1].text)
	rank = clean_string(line[3].text)
	i = 0
	found = False
	while(True):
		if(name in conference_name):
			return rank
		if(conference_name[i] != name[i]):
			#print(conference_name[i], "!=", name[i])
			return ""
		else:
			#print(conference_name[i], "==", name[i])
			i+=1
		if(i == len(conference_name)):
			return rank


def display_rank_conference(conference_name):
	"""
	Simple fonction de test permettant de tester rapidement la fonction get_rank()

	@param
	journal_name : string, nom du journal
	"""
	print("DISPLAY_RANK | Conference :",conference_name,", rank :",get_rank_conference(conference_name))


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
							conference_name = article_data.text
						if(article_data.tag == "year"):
							annee = article_data.text
						if(article_data.tag == "title"):
							titre = article_data.text
						if(article_data.tag == "author"):
							name = re.sub(r'[0-9]*', '', article_data.text)
							auteur_liste += name+", "
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


def get_lieux(conference_url):
	"""
	Retourne une liste de 2 elements ['Pays', 'Etat, 'Ville'] correspondant au lieu de conference

	@param
	conference_url : string, url extrait d'un fichier xml d'un auteur ex: "db/conf/sss/sss2011.html#AlonADDPT11"
	"""
	if("db/journals/" in conference_url):
		return ['','','']
	url = "https://dblp.uni-trier.de/"+conference_url
	#proxy = {"https":"https://proxy.ufr-info-p6.jussieu.fr:3128"}
	element_splited_lieux = ""
	page = requests.get(url) # , proxies=proxy)
	soup = BeautifulSoup(page.content, "html.parser")
	res = soup.find_all('h1')
	for elem in res:
		element_splited = elem.text.split(':') #\n
		element_splited_lieux = element_splited[1]
		element_splited_lieux2 = element_splited_lieux.replace('\n', '')
		return element_splited_lieux2.replace(' ', '').split(',')
		

def display_lieux_conf(conference_url):
	"""
	Simple fonction permettant de tester get_lieux plus facilement

	@param
	conference_url : string, lien (dblp) vers la conference ex: "db/conf/sss/sss2011.html#AlonADDPT11"
	"""
	tab = get_lieux(conference_url)
	string = "Unknown"
	if(len(tab) >= 2 and tab[0]):
		string = "Pays:"+tab[0]
	if(len(tab) == 3 and tab[1]):
		string += " Etat:"+tab[1]
		if(tab[2]):
			string += " Ville:"+tab[2]
	else:
		if(tab[1]):
			string += " Ville:"+tab[1]
	print(string)


def conf_voyages(author_name):
	"""
	Retourne un tableau contenant des elements : [ [Ville, Etat, Pays], Conf_name, annee]
	(utile pour simplifier l'affichage de la carte de la question 7)

	@param
	author_name : string, nom de l'auteur (nom+' '+prenom)
	"""
	liste_conf = liste_resume_conference("Auteurs/"+author_name+".xml")
	#liste_conf => [conf_name, annee, url]
	if(len(liste_conf) <= 0):
		print("error taille liste [conf_voyages()]")
		return -1
	else:
		tab = []
		for elem in liste_conf:
			#if(len(elem) != 0):
			tab.append([get_lieux(elem[2]), elem[0], elem[1]])
		for e in tab:
			print(e)
		return tab

	#get_lieux(conference_url)


#-------------------------------------------------------
#			Fonctions utilitaires diverses
#-------------------------------------------------------
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






if __name__ == '__main__':

	#https://dblp.uni-trier.de/pers/xx/b/Bazargan=Sabet:Pirouz.xml
	#https://dblp.uni-trier.de/pers/xx/b/Bazargan=Sabet:Pirouz.xml

	#print(request_author_file_builder("Pirouz Bazargan Sabet", "table_html.txt"))

	"""
	#TEST START
 	#--Tests de la partie récupération du fichier sur internet
	print("<--TESTS TELECHARGEMENT DE FICHIER XML-->")
	print("		Test création dictionnaire html : ",len(create_dico_html("table_html.txt")) == 103)
	print("		Test création url pour le fichier XML de 'Sébastien Baey' :", request_author_file_builder("Sébastien Baey", "table_html.txt") == "https://dblp.uni-trier.de/pers/xx/b/Baey:S=eacute=bastien.xml")
	#print("		Test de téléchargement du fichier de 'Sébastien Baey' : ",download_file("Sébastien Baey", "Auteurs/", "table_html.txt"))

	#--Tests de la partie de traitement du fichier XML
	print("<--TESTS TRAITEMENT DE FICHIER XML-->")
	print("		Test création dictionnaire iso : ",len(create_dico_iso("table_iso.txt")) == 267)
	print("		Test decoupage complet d'une ligne avec des codes iso : ", split_char_code("<title>&truc muche&456; code iso & un autre truc</title>") == ['<title>', '&', 'truc muche', '&456;', ' code iso ', '&', ' un autre truc</title>'])
	print("		Test remplacement caractere special : ", replace_char(["truc ", "&#233;", " muche"], create_dico_iso("table_iso.txt")) == "truc é muche")
	print("		Test découpe caratere de fin de ligne :", cut_end("blablabla truc\n") == "blablabla truc")
	print(split_char_code("Browsing, Sharing, Learning and Reviewing the Haine du th&#233;&#226;tre Corpus through Insightful Island."))
	#TEST END
	"""

	#AUTRES TESTS
	#print(request_author_file_builder("Pierre Sens", "table_html.txt"))
	#download_file("Christophe Gonzales", "Auteurs/", "table_html.txt")
	#xml_formater("Auteurs/Christophe Gonzales.xml", "Auteurs/_Christophe Gonzales.xml", create_dico_iso("table_iso.txt"))
	"""
	display_rank_journal("CoRR")
	display_rank_journal("J. Parallel Distrib. Comput.")
	display_rank_journal("IEEE Trans. Parallel Distrib. Syst.")
	display_rank_journal("Algorithmica")
	display_rank_journal("Compute J")
	display_rank_journal("J. Comput. Syst. Sci.")
	display_rank_journal("Theor. Comput. Sci.")
	display_rank_journal("Computer Networks")
	display_rank_journal("Neurocomputing")
	display_rank_journal("")
	print()
	display_rank_conference("OPODIS")
	display_rank_conference("DISC")
	display_rank_conference("ICDCS")
	display_rank_conference("PODC")
	display_rank_conference("CTW")
	display_rank_conference("")	
	
	display_lieux_conf("db/conf/wdag/disc2011.html#DuboisMT11")
	display_lieux_conf("db/journals/corr/corr1103.html#abs-1103-3515")
	display_lieux_conf("db/conf/opodis/opodis2010.html#DuboisPNT10")
	display_lieux_conf(("db/conf/wdag/disc2010.html#DuboisMT10"))
	"""
	#get_coauteurs("Auteurs/Sébastien Tixeuil.xml")
	#print(liste_resume_conference("Auteurs/Olivier Fourmaux.xml"))
	#conf_voyages("Julien Sopena")
	#print(get_rank_conference("USENIX Annual Technical Conference"))

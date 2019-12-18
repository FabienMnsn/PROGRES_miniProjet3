import requests
import re
import os


#------------------------------------------------------------------------------------------------------------
# Fonctions permettant de, télécharger et traiter un fichier XML avant de pouvoir lancer le parser ElementTree
#------------------------------------------------------------------------------------------------------------


#------------------------------FONCTIONS DE RECUPERATION DU FICHIER SOURCE
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
	last_name_cut = author_name_split[1][0].lower()
	request = "https://dblp.uni-trier.de/pers/xx/"+last_name_cut+"/"+author_name_split[1]+":"+author_name_split[0]+".xml"
	return request


def download_file(author_name, download_path, table_path):
	"""
	Telecharge et parse un fichier xml correspondant au nom de l'auteur passe en parametre.

	@param
	author_name : string représentant le nom et le prénom d'un auteur  ex:"Prenom Nom"
	download_path : chemin d'accès du repertoire ou le fichier sera téléchargé ex:"XML/downloads/"
	"""
	requested = requests.get(request_author_file_builder(author_name, table_path))
	file_name = download_path+"_"+author_name+".xml"
	if(requested.status_code == 200):
		with open(file_name, 'wb') as local_file:
			for chunk in requested.iter_content(chunk_size=128):
				local_file.write(chunk)
		local_file.close()
		parse_file(file_name, download_path+author_name+".xml", "table_iso.txt")
		os.remove(file_name)
	else:
		print(requested.status_code)
	return requested.status_code
#------------------------------FIN DES FONCTIONS DE RECUPERATION DU FICHIER SOURCE



#------------------------------FONCTIONS DE TRAITEMENT DU FICHIER SOURCE
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
        if('&' in elem and elem[0] == '&' and elem[-1] != ';'):
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
        else:
            contains_special_char = re.search(r"&", line_)
            if(contains_special_char != None and len(contains_special_char[0]) > 0):
                splited_line = split_char_code(line_)
                new_line = replace_char(splited_line, dictio)
                new_xml.write(new_line+"\n")
            else:
                new_xml.write(line_+"\n")
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



if __name__ == '__main__':

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
	#TEST END


	#AUTRES TESTS
	print(request_author_file_builder("Christophe Gonzales", "table_html.txt"))
	download_file("Christophe Gonzales", "Auteurs/", "table_html.txt")
	xml_formater("Auteurs/Christophe Gonzales.xml", "Auteurs/_Christophe Gonzales.xml", create_dico_iso("table_iso.txt"))

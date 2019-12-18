import requests
import re
import os

#imported from our project :
import xml_file_transcoding


def create_dico_html(caracter_table_file_path):
	"""
	Cree un dictionnaire des codes html correspondnats au caracteres speciaux

	@param
	caracter_table_file_path = "/Doxuments/table_html.txt"
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
	Retourne un url de requete donnant aucces au fichier xml correspondant au nom de l auteur en parametre
	
	@param
	author_name = "Prenom Nom"
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
	author_name = "Prenom Nom"
	download_path = "XML/downloads/"
	"""
	requested = requests.get(request_author_file_builder(author_name, table_path))
	file_name = download_path+"_"+author_name+".xml"
	if(requested.status_code == 200):
		with open(file_name, 'wb') as local_file:
			for chunk in requested.iter_content(chunk_size=128):
				local_file.write(chunk)
		local_file.close()
		xml_file_transcoding.parse_file(file_name, download_path+author_name+".xml", "table_iso.txt")
		os.remove(file_name)
	else:
		print(requested.status_code)
	return requested.status_code


if __name__ == '__main__':

	#TESTS START
	#print(request_author_file_builder("Sébastien Baey", "table_html.txt"))
	#pb avec les accents => solution : changer la fonction de creation d'url
	author_name = input("Entrez un nom de chercheur :")
	download_file(author_name, "Auteurs/", "table_html.txt")
	#di = create_dico_html("table_html.txt")
	#print(di["é"])
	#TESTS END
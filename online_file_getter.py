import requests
import re
import os

#imported from our project :
from xml_file_transcoding import *

def request_author_file_builder(author_name):
	"""
	Retourne un url de requête donnant aucces au fichier xml correspondant au nom de l'auteur en paramètre
	
	@param
	author_name = "Prenom Nom"
	"""
	author_name_split = author_name.split(' ')
	last_name_cut = author_name_split[1][0].lower()
	request = "https://dblp.uni-trier.de/pers/xx/"+last_name_cut+"/"+author_name_split[1]+":"+author_name_split[0]+".xml"
	return request


def download_file(author_name, download_path):
	"""
	Télécharge et parse un fichier xml correspondant au nom de l'auteur passé en paramètre.

	@param
	author_name = "Prenom Nom"
	download_path = "XML/downloads/"
	"""
	requested = requests.get(request_author_file_builder(author_name))
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


if __name__ == '__main__':
	print(request_author_file_builder("Sebastien Baey"))
	#pb avec les accents => solution : changer la fonction de réation d'url
	#download_file("S=eacute=bastien Baey", "XML/")
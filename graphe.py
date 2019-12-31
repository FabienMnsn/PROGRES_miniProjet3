#---------------------------
import utils_xml
#---------------------------
import math
import os
import xml.etree.ElementTree as ET
#import networkx as nx
#from sagemath import *
#from sage.all import *
#import matplotlib.pyplot as plt
#import random





def list_all_publication(author_name1, author_name2):
	"""
	Retourne un dictionnaire contenant les lien de publication entre tous les membres permanents du lip6

	@param
	author_name1 : string, nom de l'auteur 1 ex:"Sébastien Tixeuil"
	author_name2 : string, nom de l'auteur 2 ex:"Olivier Fourmaux"
	"""
	links = {}
	found = 0 
	lip6 = utils_xml.liste_lip6("Auteurs/lip6.xml")
	for i in lip6:
		if(i == author_name1 or i == author_name2):
			found += 1
		else:
			continue
	if(found != 2):
		print("Un des deux auteur n'est pas bien orthographié ou n'est pas un membre permanent du lip6")
		return -1
	else:
		list_file = os.listdir("Auteurs/")
		if(author_name1+".xml" not in list_file):
			print("telechargement du fichier de :", author_name1)
			utils_xml.download_file(author_name1, "Auteurs/", "table_html.txt")
		if(author_name2+".xml" not in list_file):
			print("telechargement du fichier de :", author_name2)
			utils_xml.download_file(author_name2, "Auteurs/", "table_html.txt")
		
		l1_coauteurs = utils_xml.get_coauteurs("Auteurs/"+author_name1+".xml")
		l2_coauteurs = utils_xml.get_coauteurs("Auteurs/"+author_name2+".xml")
		
		L1 = []
		for aut in l1_coauteurs:
			if(aut in lip6):
				L1.append(aut)
		links[author_name1] = L1

		L2 = []
		for aut in l2_coauteurs:
			if(aut in lip6):
				L2.append(aut)
		links[author_name2] = L2

		#print(l1_coauteurs)
		print(links)


def get_links(lip6_members_path):
	"""
	Retourne un dictionnaire ou chaque cle est un membre premanent du lip6 et la valeur associée a la clée est la liste des coauteurs qui sont aussi membres permanents du lip6
	
	@param
	lip6_members_path : string, chemin d'acces du fihcer xml des membres permanents du lip6
	"""
	echec = 0
	links = {}
	lip6 = utils_xml.liste_lip6(lip6_members_path)
	if(len(lip6) == 0):
		return -1
	list_file = os.listdir("Graphe/")
	for member in lip6:
		if(member+".xml" not in list_file):
			#print("telechargement du fichier de :", member)
			ret = utils_xml.download_file(member, "Graphe/", "table_html.txt")
			if(ret == 404):
				echec += 1
				continue
		coauteurs = utils_xml.get_coauteurs("Graphe/"+member+".xml")
		ltmp = []
		for aut in coauteurs:
			if(aut in lip6):
				ltmp.append(aut)
		links[member] = ltmp
	#i = 0
	#for elem in links:
		#i += 1
		#print(i, elem, links[elem])
	print("Impossible de récupérer", echec, "/", len(lip6), "fichiers (dead links in dblp)")


def draw_graph(links_dico):
	"""
	Retourne un graphe reseau des publications entre membres permanents du lip6

	@param
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	"""


if __name__ == '__main__':

	get_links("Auteurs/lip6.xml")
	#print(liste_lip6("Auteurs/lip6.xml"))
	#http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph.html#graph-format

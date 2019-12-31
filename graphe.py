#---------------------------
import utils_xml
#---------------------------
import os
import networkx as nx
#from sagemath import *
#from sage.all import *
import matplotlib.pyplot as plt



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
	#print(links.keys())
	#print("Impossible de récupérer", echec, "/", len(lip6), "fichiers (dead links in dblp)")
	return links


def draw_graph(lip6_members_path, links_dico, author_name1, author_name2):
	"""
	Retourne un graphe reseau des publications entre membres permanents du lip6

	@param
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	author_name1 : string nom de l'auteur1 ex : "Prénom Nom"
	author_name2 : string nom de l'auteur2 ex : "Prénom Nom"
	"""
	lip6 = utils_xml.liste_lip6(lip6_members_path)
	if(author_name1 in lip6 and author_name2 in lip6):
		G = nx.Graph()
		color = []
		node_labels = {}
		for key in links_dico.keys():
			if(key == author_name1):
				node_labels[author_name1] = author_name1.replace(' ', '\n')
				color.append("red")
			elif(key == author_name2):
				node_labels[author_name2] = author_name2.replace(' ', '\n')
				color.append("orange")
			else:
				color.append("blue")
			G.add_node(key)
		plt.figure(figsize=(10,10))
		nx.draw(G, with_labels=True, labels=node_labels, node_color=color, font_size=7)
		plt.show()
	else:
		print("ERROR : incorrect name authors")

if __name__ == '__main__':

	draw_graph("Auteurs/lip6.xml", get_links("Auteurs/lip6.xml"), "Olivier Fourmaux", "Julien Sopena")
	#print(liste_lip6("Auteurs/lip6.xml"))
	#http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph.html#graph-format

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


def draw_graph_2membres(author_name1, author_name2):
	"""
	Retourne un graphe reseau des publications entre membres permanents du lip6

	@param
	lip6_members_path : string, chemin d'acces du ficher xml des membres permanents du lip6 
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	author_name1 : string nom de l'auteur1 ex : "Prénom Nom"
	author_name2 : string nom de l'auteur2 ex : "Prénom Nom"
	"""
	lip6 = utils_xml.liste_lip6("Auteurs/lip6.xml")
	links_dico = get_links("Auteurs/lip6.xml")
	if(author_name1 in lip6 and author_name2 in lip6):
		G = nx.Graph()
		color = []
		node_labels = {}
		nodes_size = []
		edges = []
		edges_color = []
		list_coaut1 = links_dico[author_name1]
		list_coaut2 = links_dico[author_name2]
		#print(list_coaut1)
		#print(list_coaut2)
		for key in links_dico.keys():
			if(key == author_name1):
				node_labels[author_name1] = author_name1.replace(' ', '\n')
				nodes_size.append(400)
				color.append("red")
			elif(key == author_name2):
				node_labels[author_name2] = author_name2.replace(' ', '\n')
				color.append("orange")
				nodes_size.append(400)
			elif(key in list_coaut1):
				color.append("red")
				node_labels[key] = key.replace(' ', '\n')
				nodes_size.append(100)
			elif(key in list_coaut2):
				color.append("orange")
				node_labels[key] = key.replace(' ', '\n')
				nodes_size.append(100)
			else:
				color.append("grey")
				nodes_size.append(15)
			G.add_node(key)

		for elem in list_coaut1:
			edges.append((author_name1, elem))
			edges_color.append("red")

		for elem in list_coaut2:
			edges.append((author_name2, elem))
			edges_color.append("orange")

		G.add_edges_from(edges)
		plt.figure(figsize=(15,8))
		nx.draw_random(G, node_size=nodes_size, with_labels=True, labels=node_labels, node_color=color, edge_color=edges_color, font_size=8, font_weight='bold')
		plt.savefig("graphe2.png", dpi=200)
		#plt.show()
	else:
		print("ERROR : incorrect name authors")


def draw_graph_all():
	"""
	Retourne rien mais enregistre une image du schéma des publication entre tous les membres permanents du lip6
	
	@param
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	"""
	#color = ["red", "blue", "green", "orange", "grey", "purple", "brown"]
	links_dico = get_links("Auteurs/lip6.xml")
	G = nx.Graph()
	edges = []
	#edges_color = []
	#index_color = 0
	for key in links_dico.keys():
		liste = links_dico[key]
		if(len(liste) != 0):
			for element in liste:
				edges.append((key,element))
				#edges_color.append(color[index_color%len(color)])
		else:
			continue
		#index_color +=1
	
	G.add_edges_from(edges)
	plt.figure(figsize=(15,15))
	poslay = nx.spring_layout(G, k=1)
	nx.draw(G, pos=poslay, with_labels=True, node_size=10, node_color="grey", edge_color="grey", width=0.5, font_size=8, font_weight='normal')
	plt.savefig("grapheAll.png", dpi=90)


if __name__ == '__main__':


	#draw_graph_2membres("Auteurs/lip6.xml", get_links("Auteurs/lip6.xml"), "Swan Dubois", "Sébastien Tixeuil")
	draw_graph_all(get_links("Auteurs/lip6.xml"))
	#print(liste_lip6("Auteurs/lip6.xml"))
	#http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph.html#graph-format

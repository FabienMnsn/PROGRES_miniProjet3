import math
#import networkx as nx
from sagemath import *
import matplotlib.pyplot as plt
import random


def draw_graphe(auteur_name1, auteur_name2):
	"""
	Dessine un graphe ou chaque point est un memebre du lip6 et les deux point de couleur differente sont les deux meembres choisis

	@param
	auteur_name1 : string, nom et prenom de l'auteur1 séparés par un espace
	auteur_name2 : string, nom et prenom de l'auteur2 séparés par un espace
	"""
	graph = nx.Graph()

	nb_added = 0
	centre = 100
	centreX = 100
	centreY = 100
	pad = 40
	random_max = 200
	rayon = 50
	#membres permanents du lip6 = 193 - les deux auteurs sélectionnés = 191
	while(nb_added < 191):
		x = random.randrange(1,random_max, 5+random.randint(1,4))
		y = random.randrange(1,random_max, 5+random.randint(1,4))
		#x = random.uniform(1,random_max)
		#y = random.uniform(1,random_max)
		distance_au_centre = math.pow((x-centreX),2)+math.pow((y-centreY),2)
		if(distance_au_centre > math.pow(rayon, 2)+pad):
			graph.add_node("N"+str(nb_added), pos=(x,y))
			nb_added +=1
		"""
		if(y < centre-pad or y > centre+pad):
			graph.add_node("N"+str(nb_added), pos=(x,y))
			nb_added +=1
		elif(x < centre-pad or x > centre+pad):
			graph.add_node(nb_added, pos=(x,y))
			nb_added +=1
		"""
	graph.add_nodes_from(['Pierre\nSens'], pos=(centre-pad/4, centre), style="filled", fillcolor='red')
	graph.add_node("Olivier\nFourmaux", pos=(centre+pad/4, centre))
	graph.add_edge('Pierre\nSens','Olivier\nFourmaux')
	graph.add_edge('Olivier\nFourmaux', 'Pierre\nSens')
	graph.add_edge('Pierre\nSens','Olivier\nFourmaux')

	pos = nx.get_node_attributes(graph, 'pos')
	nx.draw(graph, pos, with_labels=True)

	#plt.savefig("path.png")
	plt.show()


def circular():
	rayon = 4
	marge = 1
	for x in range(-10, 10):
		for y in range(-10, 10):
			x2 = math.pow(x, 2)
			r2 = math.pow(rayon, 2)
			y2 = x2 - r2
			if((x2+y2) > (r2-marge) and (x2+y2) < (r2+marge)):
				print("eq res :")


if __name__ == '__main__':

	#draw_graphe("hsfkjsfhe", "hsfjksh")

	#http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph.html#graph-format

	d = {0: [1,4,5], 1: [2,6], 2: [3,7], 3: [4,8], 4: [9], 5: [7, 8], 6: [8,9], 7: [9]}
	G = Graph(d)
	G.plot().show()
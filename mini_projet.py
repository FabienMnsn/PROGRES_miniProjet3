#import xml.etree.ElementTree as ET
from lxml import etree
import bottle
from bs4 import BeautifulSoup

#parsing du fichier XML

"""
#marche pas a cause des '&' et des '#' qui font crash le parser
tree = ET.parse('dblp.xml')
root = tree.getroot()
for child in root:
        print(child.tag)
        break

#marche pas non plus et prend environ 12Go de ram pour tourner...
dblp = open("dblp.xml", "r")
soup = BeautifulSoup(dblp, "xml")
res = soup.find('dblp')
print(res)

marche pas non plus meme en ouvrant le fichier avec le bon encodage...
dblp = open('dblp.xml', 'r', encoding="iso-8859-1")
tree = etree.parse(dblp)
i = 0
for elem in tree:
        if(i > 10):
                break
        print(i)
        print(elem)
        i+=1
"""

import xml.etree.ElementTree as ET


"""
tentative de charger l'extrait du fichier dblp.xml
"""

tree = ET.parse('XML/PARSED_extract_dblp.xml')
root = tree.getroot()
for child in root:
    print(child.tag)
    for grandchild in child:
        print(grandchild.tag)
    break

"""
with open("XML/dblp.xml", 'r') as f:
    content = f.read()

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

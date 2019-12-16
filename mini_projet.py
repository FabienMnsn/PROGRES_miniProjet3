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

#--------------------------FONCTION BOTTLE--------------------------


@bottle.route("/auteur/qui")
@bottle.view("page.tpl")
def qui():
    stri = """
    <form method='post' action='name'>
    <input type='text' name='last_name' placeholder='Nom'/>
    <input type='text' name='first_name' placeholder='Prénom'/>
    <input type='submit' value='Chercher'/>
    </form>
    """
    return {"title":"Rechercher un auteur", "body":stri}



@bottle.route("/auteur/name", method='POST')
@bottle.view("page.tpl")
def name():
    lname = bottle.request.forms.last_name
    fname = bottle.request.forms.first_name
    return {"title":"Vous consultez la page de ", "body": fname+", "+lname}


#--------------------------RUN BOTTLE--------------------------
bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
#--------------------------RUN BOTTLE--------------------------

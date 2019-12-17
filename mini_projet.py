#import xml.etree.ElementTree as ET
import xml_file_loader
from lxml import etree
import bottle
from bottle import redirect
from bs4 import BeautifulSoup

#parsing du fichier XML

"""
#marche pas a cause des '&' et des '#' qui font crash le parser

"""

#--------------------------FONCTION BOTTLE--------------------------


@bottle.route("/auteur/qui")
@bottle.view("page.tpl")
def auteur():
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
    redirect("/auteur/"+lname+"/"+fname)

@bottle.route("/auteur/<lname>/<name>")
@bottle.view("page.tpl")
def auteur(lname,name):
    dico=xml_file_loader.publication_stat("Auteurs/"+name+" "+lname+".xml")
    stri="""  <table style="width:15%">
    <tr>
    <td>Nombre journaux</td>"""+"<td>"+str(dico["journaux"])+"""</td>
    </tr>
    <tr>
    <td>Nombre conference</td>"""+"<td>"+str(dico["conferences"])+"""</td>
    </tr>
    <tr>
    <td>Nombre de co-auteur</td>"""+ "<td>"+str(dico["co-auteurs"])+"""</td>
    </tr>
    </table>"""
    
    return {"title":"Vous consultez la page de "+name+" "+lname, "body":" les stats de la personne    "+stri}


#--------------------------RUN BOTTLE--------------------------
bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
#--------------------------RUN BOTTLE--------------------------

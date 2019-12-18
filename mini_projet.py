#---------------------------
import xml_file_loader
import online_file_getter
#---------------------------
import os
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
    list_file = os.listdir("Auteurs/")
    author_name = name+" "+lname
    file_name = author_name+".xml"
    if(file_name not in list_file):
        #si le fichier n'existe pas on le telecharge
        status = online_file_getter.download_file(author_name, "Auteurs/", "table_html.txt")
        if(status != 200):
            #error(status, message)
            print(status)
            return
    dico=xml_file_loader.publication_stat("Auteurs/"+file_name)

    stri="""<div><table style="border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse">
    <caption>Statistiques générales</caption>
    <tr>
    <td style="border:1px solid black;padding:10px">Nombre de journaux</td>"""+"<td style='border:1px solid black;padding:10px'>"+str(dico["journaux"])+"""</td>
    </tr>
    <tr>
    <td style='border:1px solid black;padding:10px'>Nombre de conferences</td>"""+"<td style='border:1px solid black;padding:10px'>"+str(dico["conferences"])+"""</td>
    </tr>
    <tr>
    <td style='border:1px solid black;padding:10px'>Nombre de co-auteurs</td>"""+ "<td style='border:1px solid black;padding:10px'>"+str(dico["co-auteurs"])+"""</td>
    </tr>
    </table></div>"""
    
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}


if __name__ == '__main__':
    #--------------------------RUN BOTTLE--------------------------
    bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
    #--------------------------RUN BOTTLE--------------------------

#---------------------------
import utils_xml
import graphe
#---------------------------
import os
from lxml import etree
import bottle
from bottle import redirect
from bottle import static_file
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium





"""
Description : Cette fonction est uniquement une décoration de la fonction download_file() du fichier utils_xml.py, elle gère en plus les differentes cas d'erreur.
Return      : Retourne une string decrivant le status de sortie de la fonction ayant les valeurs : 'ok', 'erreur' et 'erreur homonymes'.
Parameters  : Aucun.
Errors      : Aucune erreur car la vérification est faite plus loins.
"""
def telecharge(author_name):
    ret_val = "ok"
    file_name = author_name+".xml"
    list_file = os.listdir("Auteurs/")
    if(file_name not in list_file):
    #si le fichier n'existe pas on le telecharge
        status = utils_xml.download_file(author_name, "Auteurs/", "table_html.txt")
        if(status != 200):
            #si le telechargement echoue on retourne une erreur
            return "erreur"
        else:
            #sinon cela veut dire que l'on a recupéré un fichier
            #on doit donc vérifier qu'il s'agit bien d'un fichier d'auteur
            file = open("Auteurs/"+file_name, "r")
            file_content = file.readlines()
            #print(file_content)
            if(len(file_content) > 30):
                return "ok"
            else:
                file.close()
                os.remove("Auteurs/"+file_name)
                return "erreur homonymes"
    #si le fichier existe
    else:
        #on vérifie qu'il contient des balises <r> qui sont des publications
        file = open("Auteurs/"+file_name, "r")
        file_content = file.readlines()
        if(len(file_content) < 30):
            #ce fichier n'est pas un fichier contenant les publication d'un auteur pb d'homonymes (personnes de meme nom)
            file.close()
            os.remove("Auteurs/"+file_name)
            return "erreur homonymes"
        else:
            file.close()
            return "ok"


#--------------------------FONCTION BOTTLE--------------------------


"""
Description : Cette fonction est la route principale de l'API.
Return      : une page html avec plusieurs liens vers les différentes routes bottle
Parameters  : Aucun.
Errors      : Aucune.
"""
@bottle.route('/')
@bottle.view("page.tpl")
def hello():
    body = """<div><a href='http://localhost:8080/auteur/qui'>[Rechercher Auteur]</a></div>
    <div><a href='http://localhost:8080/Conference/Laquelle'>[Rechercher Conference]</a></div>
    <div><a href='http://localhost:8080/LIP6'>[Graphe publication Lip6]</a></div>
    <div><a href='http://localhost:8080/LIP6/auteurs'>[Graphe publication 2 auteurs]</a></div>"""
    return { "title":"Menu API", "body": body}




"""
Description : Cette fonction fabrique un formulaire de saisie html minimaliste demandant de saisir le nom et le prénom d'un auteur.
Return      : Un formulaire dans une page html.
Parameters  : Aucun.
Errors      : Aucune erreur car la vérification est faite plus loins.
"""
@bottle.route("/auteur/qui")
@bottle.view("page.tpl")
def auteur():
    stri = """<div><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <div><a href='http://localhost:8080/Conference/Laquelle'>[Rechercher Conference]</a></div>
    <form method='post' action='name'>
    <input type='text' name='last_name' placeholder='Nom'/>
    <input type='text' name='first_name' placeholder='Prénom'/>
    <input type='submit' value='Chercher'/>
    </form>
    """
    return {"title":"Rechercher un auteur", "body":stri}




"""
Description : Cette fonction fait uniquement une redirection vers une autre route.
Return      : Rien.
Parameters  : Aucun.
Errors      : Aucune erreur car la vérification est faite plus loins dans la fonction d'après.
"""
@bottle.route("/auteur/name", method='POST')
@bottle.view("page.tpl")
def name():
    lname = bottle.request.forms.last_name
    fname = bottle.request.forms.first_name
    redirect("/auteur/"+lname+"_"+fname)




"""
Description : Cette fonction fabrique une table html et la retourne si l'auteur a été trouvé dans la base dblp sinon elle renvoie une erreur.
Return      : Table html a 3 lignes, nombre de journaux, nombre de conference et nombre de co-auteurs.
Parameters  : name -> le nom de l'auteur que l'on recupère grâce à la fonction de redirection au dessus.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/<name>")
@bottle.view("page.tpl")
def auteur(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.publication_stat("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
    	return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    dico=utils_xml.publication_stat("Auteurs/"+file_name)

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
    </table></div>
    <div align='center'><a href='http://localhost:8080/'>[Menu principal]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/Journals/synthese/"""+name+"""'>[Journals synthese]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/Journals/"""+name+"""'>[Journals detail]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/Conferences/synthese/"""+name+"""'>[Conference synthese]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/Conferences/"""+name+"""'>[Conference detail]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/Conferences/Voyages/"""+name+"""'>[Conference Voyage]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/coauthors/"""+name+"""'>[Coauthors]</a></div>
    """
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction retourne une page html contenant un tableau présentants les publications selon leur rang Core (un rang par colonne).
Return      : Une page html avec une table des publications dans chaque case on trouve le nom et l'année de la publication.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/Journals/synthese/<name>")
@bottle.view("page.tpl")
def synthese(name):
    name_split = name.split("_")
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_resume_publication("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    liste_art={}
    liste_nb_rang={}
    liste_annee_art={}
    keys=["A*","A","B","C","Unranked"]
    dico={key: [] for key in keys}
    for pub in tab:
        try:
            liste_nb_rang[utils_xml.get_rank_journal(pub[1])]+=1
        except:
            liste_nb_rang[utils_xml.get_rank_journal(pub[1])]=1
        try :
            liste_art[pub[1]]+=1
        except:
            liste_art[pub[1]]=1
        if liste_art[pub[1]]==1:
            
            dico[utils_xml.get_rank_journal(pub[1])].append(pub[1])
        try:
            if pub[0] not in liste_annee_art[pub[1]]:

                liste_annee_art[pub[1]].append(pub[0])
        except:
            liste_annee_art[pub[1]]=[]
            liste_annee_art[pub[1]].append(pub[0])
    total = 0

    for k in keys:
        try :
            total+=liste_nb_rang[k]
        except:
            pass

    stri = """<div align='center'><a href='http://localhost:8080/'>[Menu Principal]</a></div><div align='center'><a href='http://localhost:8080/auteur/"""+name+"""'>[Menu Auteur]</a></div>"""
    if(total > 1):
    	stri+="<div><h3 align='center'>   "+str(total)+" Articles publiés</h3></div>"
    else:
    	stri+="<div><h3 align='center'>   "+str(total)+" Article publié</h3></div>"
    stri+="<div align='center'><a href='http://localhost:8080/auteur/Conferences/synthese/"+name+"'>[Conférences]</a></div>"

    stri+="""<div align='center'><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
        <caption>Liste détaillée des articles</caption><tr>"""

    for i in dico.keys():
        try:
            stri+="<th style='border:1px solid black'>"+i+" ("+str(liste_nb_rang[i])+") </th>"
        except:
            stri+="<th style='border:1px solid black'>"+i+" (0) </th>"
    
    stri+="</tr>"

    taillekey=[]
    for k in keys:
        try:
            taillekey.append(len(dico[k]))
        except:
            pass
    m=max(t for t in taillekey)
    
    for j in range(m):
        stri+="<tr>"
        for k in keys:
            try:
                tmp=dico[k][j]
                str_annee=None
                for i in liste_annee_art[tmp]:
                    try:
                        str_annee+=", "+i
                    except:
                        str_annee=i
                stri+="<td style='border:1px solid black;padding:10px'>"+tmp+" ("+str(liste_art[tmp])+")  ("+str_annee+") </td>"

            except:
                tmp=""
                stri+="<td style='border:1px solid black;padding:10px'>"+tmp+"</td>"
        stri+="</tr>"

    stri+="</table></div>"

    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction retourne une page html détaillant toutes les publications d'un auteur.
Return      : Page html contenant une table html avec une ligne par publication et quatre colonnes : nom de l'article, auteurs, nom du journal et année de publication.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/Journals/<name>")
@bottle.view("page.tpl")
def journal(name):
    name_split = name.split("_")
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_detail_publication("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    stri="""<div align='center'><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/"""+name+"""'>[Menu Auteur]</a></div>
    <div align='center'><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <div align='center'><a href='http://localhost:8080/auteur/Conferences/"""+name+"""'>[Conférences]</a></div>
    <caption>Liste détaillée des publications ("""+str(len(tab))+""")</caption>
    <tr>
    <th style='border:1px solid black'>Article</th>
    <th style='border:1px solid black'>Auteur</th>
    <th style='border:1px solid black'>Journal</th>
    <th style='border:1px solid black'>Annee</th>
    </tr>"""
    for pub in tab:
            stri+=" <tr><td style='border:1px solid black;padding:10px'>"+pub[0]+"</td><td style='border:1px solid black;padding:10px'>"+pub[1]+"</td>"
            stri+=" <td style='border:1px solid black;padding:10px'>"+pub[2]+"</td><td style='border:1px solid black;padding:10px'>"+pub[3]+"</td></tr>"

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction retourne une page html contenant un tableau présentants les conférences selon leur rang Core (un rang par colonne). 
Return      : Une page html avec une table des conférences dans chaque case on trouve le nom et l'année de la conférence.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/Conferences/synthese/<name>")
@bottle.view("page.tpl")
def conferences(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_resume_conference("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}

    liste_conf={}
    liste_nb_rang={}
    liste_annee_conf={}
    keys=["A*","A","B","C","Unranked"]
    dico={key: [] for key in keys}
    for pub in tab:
        try:
            liste_nb_rang[utils_xml.get_rank_conference(pub[0])]+=1
        except:
            liste_nb_rang[utils_xml.get_rank_conference(pub[0])]=1
        try :
            liste_conf[pub[0]]+=1
        except:
            liste_conf[pub[0]]=1
        if liste_conf[pub[0]]==1:
            dico[utils_xml.get_rank_conference(pub[0])].append(pub[0])
        try:
            if pub[1] not in liste_annee_conf[pub[0]]:
                liste_annee_conf[pub[0]].append(pub[1])
        except:
            liste_annee_conf[pub[0]]=[]
            liste_annee_conf[pub[0]].append(pub[1])

    total = 0
    for k in keys:
        try :
            total+=liste_nb_rang[k]
        except:
            pass
    stri = """<div align='center'><a href='http://localhost:8080/'>[Menu Principal]</a></div><div align='center'><a href='http://localhost:8080/auteur/"""+name+"""'>[Menu Auteur]</a></div>"""
    if(total > 1):
    	stri+="<div><h3 align='center'>   "+str(total)+" Conférences </h3></div>"
    else:
        stri+="<div><h3 align='center'>   "+str(total)+" Conférence </h3></div>"
    stri+="<div align='center'><a href='http://localhost:8080/auteur/Journals/synthese/"+name+"'>[Articles]</a></div>"

    stri+="""<div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
        <caption>Liste resumée des conférences classées selon Core</caption><tr>"""

    for i in dico.keys():
        try:
            stri+="<th style='border:1px solid black'>"+i+" ("+str(liste_nb_rang[i])+") </th>"
        except:
            stri+="<th style='border:1px solid black'>"+i+"(0) </th>"
    stri+="</tr>"


    taillekey=[]
    for k in keys:
        try:
            taillekey.append(len(dico[k]))
        except:
            pass
    m=max(t for t in taillekey)


    for j in range(m):
        stri+="<tr>"
        for k in keys:
            try:
                tmp=dico[k][j]
                str_annee=None
                for i in liste_annee_conf[tmp]:
                    try:
                        str_annee+=", "+i
                    except:
                        str_annee=i
                stri+="<td style='border:1px solid black;padding:10px'>"+tmp+" ("+str(liste_conf[tmp])+")  ("+str_annee+") </td>"

            except:
                tmp=""
                stri+="<td style='border:1px solid black;padding:10px'>"+tmp+"</td>"
        stri+="</tr>"

    stri+="</table></div>"

    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction retourne une page html détaillant toutes les conférences d'un auteur. 
Return      : Page html contenant une table html avec une ligne par conférence et quatre colonnes : titre de la conférence, auteurs, nom de la conférence et année de la conférence.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/Conferences/<name>")
@bottle.view("page.tpl")
def confdetail(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_detail_conference("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    
    stri="""<div align='center'><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/"""+name+"""'>[Menu Auteur]</a></div>
    <div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <div align='center'><a href='http://localhost:8080/auteur/Journals/"""+name+"""'>[Articles]</a></div>
    <caption>Liste détaillée des conférences ("""+str(len(tab))+""")</caption>
    <tr>
    <th style='border:1px solid black'>Titre</th>
    <th style='border:1px solid black'>Auteur</th>
    <th style='border:1px solid black'>Conference</th>
    <th style='border:1px solid black'>Annee</th>
    </tr>"""

    for pub in tab:
        stri+=" <tr><td style='border:1px solid black;padding:10px'>"+pub[0]+"</td><td style='border:1px solid black;padding:10px'>"+pub[1]+"</td>"
        stri+=" <td style='border:1px solid black;padding:10px'>"+pub[2]+"</td><td style='border:1px solid black;padding:10px'>"+pub[3]+"</td></tr>"

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction retourne une page html avec une carte des différents lieux de conférences d'un auteur.
Return      : Une page html avec une carte Folium contenant des Markers GPS.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/Conferences/Voyages/<name>")
@bottle.view("page.tpl")
def conference_voyage(name):
    name_split = name.split("_")
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.conf_voyages("Auteurs/"+file_name)
        gps = utils_xml.address_to_gps(tab)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    sumX = 0
    sumY = 0
    for elem in gps:
        if(elem[0] == None):
            continue
        sumX += elem[1][0]
        sumY += elem[1][1]

    zoomX = sumX/len(gps)
    zoomY = sumY/len(gps)
    # un element du tableau gps : [['Budapest', 'Hungary'], [47.4983815, 19.0404707], 'DISC', '2019']
    map = folium.Map(location=[zoomX, zoomY], zoom_start=2)
    for elem in gps:
        if(elem[0] == None):
            continue
        conf_name = elem[2]
        ville = elem[0][0]
        annee = elem[3]
        folium.Marker(elem[1],
            popup=conf_name+' '+ville+' '+annee).add_to(map)
    body = "<div><a href='http://localhost:8080/'>[Menu Principal]</a></div><div><a href='http://localhost:8080/auteur/"+name+"'>[Menu Auteur]</a></div>"
    body += map.get_root().render()
    return { "title":"Carte des lieux de conférence de : "+author_name, "body": body}




"""
Description : Cette fonction retourne une page html présentant une table de tous les co-auteurs de l'auteur.
Return      : Page html contenant une table html avec une ligne par auteur.
Parameters  : name -> string, nom de l'auteur.
Errors      : 2 erreurs possibles sous forme de page html : Récupération des données impossible, Plusieurs auteurs au nom identique.
"""
@bottle.route("/auteur/coauthors/<name>")
@bottle.view("page.tpl")
def coauthors(name):
    name_split = name.split("_")
    author_name = name_split[1]+" "+name_split[0]
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.get_coauteurs("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Erreur : il existe plusieurs auteurs ayants le même nom", "body":"<div>Aide : Veuillez préciser l'auteur en ajoutant '+0001' apres le nom de l'auteur, par exemple : 'Sens+0001 Pierre'.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    else:
        return {"title":"Erreur : impossible de récupérer les informations de cette personne", "body":"<div>Aide : Vérifiez l'orthographe des nom et prénom de l'auteur et réessayez.</div><div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}

    stri="""<div align='center'><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <div align='center'><a href='http://localhost:8080/auteur/"""+name+"""'>[Menu Auteur]</a></div>
    <div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <caption>Liste des co-auteurs ("""+str(len(tab))+""")</caption>
    <tr>
    <th style='border:1px solid black'>Prénom Nom</th>
    </tr>"""

    for author in tab:
        stri+=" <tr><td style='border:1px solid black;padding:10px'>"+author+"</td></tr>"

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}




"""
Description : Cette fonction fabrique un formulaire de saisie de l'acronyme d'une conférence et le retourne dans une page html.
Return      : Page html contenant le formulaire.
Parameters  : Aucun.
Errors      : Aucune.
"""
@bottle.route("/Conference/Laquelle")
@bottle.view("page.tpl")
def laquelle():
    stri = """<div><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <div><a href='http://localhost:8080/auteur/qui'>[Rechercher Auteur]</a></div>
    <form align='center' method='post' action='recup_conf'>
    <input type='text' name='conference' placeholder='Conference'/>
    <input type='submit' value='Chercher'/>
    </form>
    """
    return {"title":"Rechercher une conférence", "body":stri}




"""
Description : Cette fonction fait simplement une redirection vers une autre route bottle.
Return      : Rien.
Parameters  : Aucun.
Errors      : Aucune.
"""
@bottle.route("/Conference/recup_conf", method='POST')
@bottle.view("page.tpl")
def recup_conf():

    conf = bottle.request.forms.conference
    redirect("/Conference/Lieux/"+conf)




"""
Description : Cette fonction Retourne une carte de tous les lieux d'une conférence.
Return      : une page html contenant une carte Folium avec des markers GPS.
Parameters  : conf -> string, acronyme de la conférence.
Errors      : Aucune.
"""
@bottle.route("/Conference/Lieux/<conf>")
@bottle.view("page.tpl")
def conference_lieux(conf):
    tab=utils_xml.conference_voyage_map(conf)

    map=folium.Map(location=utils_xml.geocoder_conf(tab[0])[0][1], zoom_start=2)

    cmpt=len(tab)
    
    for i in tab:
        gps=utils_xml.geocoder_conf(i)
        if gps=="pb":
            continue
        annee=gps[0][-1]
        ville=gps[0][0][0]
        #print(ville)
        #print(gps[0][1])
        if i[-2]=="oui":
            folium.Marker(gps[0][1],popup=str(i[-3])+" conference,\n"+ville+', '+annee).add_to(map)
        else:
            folium.Marker(gps[0][1],popup=ville+' '+annee).add_to(map)
    body = "<div><a href='http://localhost:8080/'>[Menu Principal]</a></div><div><a href='http://localhost:8080/Conference/Laquelle'>[Rechercher Conference]</a></div>"
    body += map.get_root().render()

    return {"title":"Carte de la conference "+conf,"body":body}




"""
Description : Cette fonction génère un graphe des relations de publication entre tous les membres du lip6.
Return      : Un graphe au format PNG.
Parameters  : Aucun.
Errors      : Aucune.
"""
@bottle.route("/LIP6")
@bottle.view("page.tpl")
def lip6():
    status = graphe.draw_graph_all()
    if(status == 0):
        return static_file("grapheAll.png", root="")
    elif(status == -1):
        return {"title":"Erreur : Fichier XML du lip6 incorrect", "body":"<div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}
    elif(status == -2):
        return {"title":"Erreur : Ouverture fichier XML lip6 impossible", "body":"<div><a href='http://localhost:8080/auteur/qui'>[Retour]</a></div>"}




"""
Description : Cette fonction fabrique un formulaire de saisie demandant de rentrer les noms et prénoms de 2 membres du lip6 (pour tracer un graphe des relations).
Return      : Une page html contenant le formulaire.
Parameters  : Aucun.
Errors      : Aucune.
"""
@bottle.route("/LIP6/auteurs")
@bottle.view("page.tpl")
def lip6_v2():
    stri = """<div><a href='http://localhost:8080/'>[Menu Principal]</a></div>
    <form align='center' method='post' action='Graphe'>
    <input type='text' name='auteur1' placeholder='Prénom Nom'/>
    <input type='text' name='auteur2' placeholder='Prénom Nom'/>
    <input type='submit' value='Générer'/>
    </form>
    """
    return {"title":"Saisissez deux auteurs :", "body":stri}




"""
Description : Cette fonction appelle la fonction qui génère le graphe du lip6 en montrant uniquement les relations des deux auteurs avec le reste du LIP6.
Return      : Un graphe au format PNG.
Parameters  : Aucun, (récupère les noms des 2 membres depuis le formulaire de saisie, string).
Errors      : Aucune.
"""
@bottle.route("/LIP6/Graphe", method='POST')
@bottle.view("page.tpl")
def Graphe():
    auteur1 = bottle.request.forms.auteur1
    auteur2 = bottle.request.forms.auteur2
    status = graphe.draw_graph_2membres(auteur1, auteur2)
    if(status == 0):
        return static_file("graphe2.png", root="")
    elif(status == -1):
        return {"title":"Erreur : Fichier XML du lip6 incorrect", "body":"<div><a href='http://localhost:8080/'>[Menu Principal]</a></div><div><a href='http://localhost:8080/LIP6/auteurs'>[Retour à la saisie]</a></div>"}
    elif(status == -2):
        return {"title":"Erreur : Ouverture fichier XML lip6 impossible", "body":"<div><a href='http://localhost:8080/'>[Menu Principal]</a></div><div><a href='http://localhost:8080/LIP6/auteurs'>[Retour à la saisie]</a></div>"}
    elif(status == -3):
        return {"title":"Erreur : Orthographe des noms incorrect ou auteurs absents des membres permanents du lip6", "body":"<div><a href='http://localhost:8080/'>[Menu Principal]</a></div><div><a href='http://localhost:8080/LIP6/auteurs'>[Retour à la saisie]</a></div>"}

#--------------------------FIN FONCTION BOTTLE--------------------------

if __name__ == '__main__':
    #--------------------------RUN BOTTLE--------------------------
    bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
    #--------------------------RUN BOTTLE--------------------------

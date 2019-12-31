#---------------------------
import utils_xml
#---------------------------
import os
from lxml import etree
import bottle
from bottle import redirect
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import folium



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
            print(file_content)
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
    #print("---->NAME :", lname, fname)
    redirect("/auteur/"+lname+"_"+fname)



@bottle.route("/auteur/<name>")
@bottle.view("page.tpl")
def auteur(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    #print("---->AUTEUR : ", author_name)
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.publication_stat("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
    	return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}
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
    </table></div>"""
    
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}



@bottle.route("/auteur/Journals/synthese/<name>")
@bottle.view("page.tpl")
def synthese(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    """
    name_split = name.split("_")
    author_name = name_split[1]+" "+name_split[0]
    """
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_resume_publication("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}

    
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

    if(total > 1):
    	stri="<div><h3 align='center'>   "+str(total)+" Articles publiés</h3></div>"
    else:
    	stri="<div><h3 align='center'>   "+str(total)+" Article publié</h3></div>"
    stri+="<div align='center'><a href='http://localhost:8080/auteur/Conferences/synthese/"+name+"'> Conférences </a></div>"

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



@bottle.route("/auteur/Journals/<name>")
@bottle.view("page.tpl")
def journal(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    """
    name_split = name.split("_")
    author_name = name_split[1]+" "+name_split[0]
    """
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_detail_publication("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}
    stri="""<div align='center'><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <div align='center'><a href='http://localhost:8080/auteur/Conferences/"""+name+"""'> Conférences </a></div>
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



@bottle.route("/auteur/Conferences/synthese/<name>")
@bottle.view("page.tpl")
def conferences(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    """
    name_split = name.split("_")
    author_name = name_split[1]+" "+name_split[0]
    """
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_resume_conference("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}

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

    if(total > 1):
    	stri="<div><h3 align='center'>   "+str(total)+" Conférences </h3></div>"
    else:
        stri="<div><h3 align='center'>   "+str(total)+" Conférence </h3></div>"
    stri+="<div align='center'><a href='http://localhost:8080/auteur/Journals/synthese/"+name+"'> Articles </a></div>"

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



@bottle.route("/auteur/Conferences/<name>")
@bottle.view("page.tpl")
def confdetail(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    """
    name_split = name.split("_")
    author_name = name_split[1]+" "+name_split[0]
    """
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.liste_detail_conference("Auteurs/"+file_name)
    elif(status=="erreur homonymes"):
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}
    
    stri="""<div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <div align='center'><a href='http://localhost:8080/auteur/Journals/"""+name+"""'> Articles </a></div>
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



@bottle.route("/auteur/Conferences/Voyages/<name>")
@bottle.view("page.tpl")
def conference_voyage(name):
    name_split = name.split("_")
    #inversion nom et prenom pour lancer la recherche
    name_h = name_split[0].replace('+', "_")
    author_name = name_split[1]+" "+name_h
    
    file_name = author_name+".xml"
    status = telecharge(author_name)
    if(status=="ok"):
        tab=utils_xml.conf_voyages("Auteurs/"+file_name)
        gps = utils_xml.address_to_gps(tab)
    elif(status=="erreur homonymes"):
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}
    sumX = 0
    sumY = 0
    for elem in gps:
        sumX += elem[1][0]
        sumY += elem[1][1]

    zoomX = sumX/len(gps)
    zoomY = sumY/len(gps)
    # un element du tableau gps : [['Budapest', 'Hungary'], [47.4983815, 19.0404707], 'DISC', '2019']
    map = folium.Map(location=[zoomX, zoomY], zoom_start=2)
    for elem in gps:
        conf_name = elem[2]
        ville = elem[0][0]
        annee = elem[3]
        #print(conf_name, ville, annee)
        folium.Marker(elem[1],
            popup=conf_name+' '+ville+' '+annee).add_to(map)
    body = map.get_root().render()
    return { "title":"Carte des lieux de conférence de : "+author_name, "body":body}


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
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":"Il existe plusieurs personnes ayant le meme nom. Veuillez préciser en ajoutant '+0001' apres le nom de l'auteur."}
    else:
        return {"title":"Oups nous n'avons pas pu récupérer les informations de cette personne", "body":""}

    stri="""<div><table style='border:1px solid black;margin-left:auto;margin-right:auto; border-collapse:collapse'>
    <caption>Liste des co-auteurs ("""+str(len(tab))+""")</caption>
    <tr>
    <th style='border:1px solid black'>Prénom Nom</th>
    </tr>"""

    for author in tab:
        stri+=" <tr><td style='border:1px solid black;padding:10px'>"+author+"</td></tr>"

    stri+="</table></div>"
    return {"title":"Vous consultez la page de : "+author_name, "body":""+stri}


@bottle.route("/Conference/Laquelle")
@bottle.view("page.tpl")
def laquelle():
    stri = """
    <form align='center' method='post' action='recup_conf'>
    <input type='text' name='conference' placeholder='Conference'/>
    <input type='submit' value='Chercher'/>
    </form>
    """
    return {"title":"Rechercher une conférence", "body":stri}


@bottle.route("/Conference/recup_conf", method='POST')
@bottle.view("page.tpl")
def recup_conf():

    conf = bottle.request.forms.conference
    #redirect("/auteur/"+lname+"/"+fname)
    redirect("/Conference/Lieux/"+conf)


@bottle.route("/Conference/Lieux/<conf>")
@bottle.view("page.tpl")
def conference_lieux(conf):
     return {"title":"Test","body":"Test"}





#--------------------------FIN FONCTION BOTTLE--------------------------

if __name__ == '__main__':
    #--------------------------RUN BOTTLE--------------------------
    bottle.run(bottle.app(), host='localhost', port='8080', debug=True, reloader=True)
    #--------------------------RUN BOTTLE--------------------------

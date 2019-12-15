import json
import re
import sys
from xml.dom import minidom

def create_dict():
    """
    fonction qui fabriue un dictionnaire a partir d'un fichier des codes html de carateres spéciaux.
    chaque clé est un code de type &uml et la valeur associée est un caractere
    """
    print("----Création du dictionnaire de référence")
    file = open('table_caracteres.txt', 'r')
    line = file.readline()
    dict = {}
    while(line != ""):
        str = line.split(';')
        key = str[1][:-1]
        value = str[0]
        if(str[1][:-1] != "Alt"):
            dict[key] = value
        line = file.readline()
    file.close()
    return dict


def split_char_code(string):
    """
    fonction qui split une chaine de caracteres en une liste de carateres.
    le critere de split est de la forme &auml; (c'est un code iso pour représenter les caracteres spéciaux)
    """
    res = []
    start_index = 0
    end_index = 0
    for i in range(len(string)):
        if(string[i] == "&"):
            end_index = i
            res.append(string[start_index:end_index])
            start_index = i
        if(string[i] == ';'):
            end_index = i+1
            res.append(string[start_index:end_index])
            start_index = i+1
        else:
            end_index = i
    res.append(string[start_index:end_index+1])
    return _extend_split_char_code(res)


def _extend_split_char_code(string):
    """
    fonction qui split un tableau de chaine de caracteres en un autre tableau de carateres en separant les & seuls.
    """
    res = []
    for elem in string:
        if('&' in elem and elem[0] == '&' and elem[-1] != ';'):
            res.append(elem[0])
            res.append(elem[1:])
        else:
            res.append(elem)
    return res


def find_index(split_string, pattern):
    """
    retourne l'index du pattern dans le tableau de string split_string, et -1 en cas d'erreur
    """
    for i in range(len(split_string)+1):
        if(pattern in split_string[i]):
            return i
    return -1


def replace_char(splited_string, dictionnaire):
    """
    remplace le string pattern dans splited _string par le charactere corespondant au motif
    s'il n'existe pas en remplace par le caractere vide
    """
    res = []
    for elem in splited_string:
        #si c'est un '&' seul on le remplace par 'and'
        if(elem == '&'):
            res.append("and")
        #si c'est un code de caractere special, on le cherche deans le dico et on le remplace
        elif('&' in elem and ';' in elem):
            if(elem[:-1] in dictionnaire):
                #elem = dico[elem[:-1]]
                res.append(dico[elem[:-1]])
            else:
                elem = ""
                res.append(elem)
        else:
            res.append(elem)
    return ''.join(res)


def cut_end(ligne):
    """
    enleve le dernier caractere de la ligne si et seulement si c'est un retour a la ligne
    """
    if(ligne[-1] == '\n'):
        return ligne[:-1]
    else:
        return ligne


def xml_formater(input_file, output_file, dictionnaire_code):
    """
    reformatage du fichier pour pouvoir le parser correctement.
    WIP => il est possible que cette fonction ne serve a rien si
    on trouve la solution pour que le parser XML dans python ne crash pas des qu'il rencontre un '&' ou un '#'...
    """
    #recuperation du dictionnaire des codes iso
    dictio = dictionnaire_code
    xml = open(input_file, 'r')
    #fichier de sortie
    new_xml = open(output_file, 'w')
    new_xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")

    print("--------Ouverture de :", input_file, ", création de :", output_file)
    for line in xml:
        #on enleve le retour chariot a la fin de la ligne s'il y en a un
        line_ = cut_end(line)
        #si c'est la ligne de definition de la version, on ne la traite pas 
        #car on la remlace par la bonne valeur au debut de la fonction xml_formater
        if("version" in line_):
            continue
        else:
            contains_special_char = re.search(r"&", line_)
            if(contains_special_char != None and len(contains_special_char[0]) > 0):
                splited_line = split_char_code(line_)
                new_line = replace_char(splited_line, dictio)
                new_xml.write(new_line+"\n")
            else:
                new_xml.write(line_+"\n")
    new_xml.close()
    xml.close()
    print("--------Fermeture des fichiers", input_file, ", ", output_file)


if __name__ == '__main__':
    #dictionnaire des codes de caracteres speciaux
    print("----------------------------------------------")
    print("Ceci est un outil qui remplace tous les caractères spéciaux par le caractère utf-8 correspondant dans un fichier XML.")
    print("Il ne marche pas à 100% sur des fichiers de plusieurs millions de lignes mais marche parfaitement sur des petits fichiers.")
    print("Il prend pas mal de ram (entre 4Go et 8Go).")
    print("Pour obtenir un fichier XML 'propre' on peut relancer l'outil en choisissant en fichier source le fichier de sortie de l'execution précédente")
    print("----------------------------------------------")
    source_file_name = input("Entrez le nom du fichier XML source (exemple : XML/dblp.xml):")
    output_file_name = input("Entrez le nom du fichier de sortie (exemple :  XML/dblp_transcoded.xml):")
    print("----------------------------------------------")
    dico = create_dict() 
    print("----Début du traitement du fichier XML")
    print("----------------------------------------------")
    xml_formater(source_file_name, output_file_name, dico)
    print("----Fin du traitement du fichier XML, le résultat se trouve dans le fichier :", output_file_name)
    print("----------------------------------------------")

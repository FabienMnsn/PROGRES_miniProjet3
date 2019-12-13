import json
import re
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
            #print(key, value)
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
            end_index = i-1
            res.append(string[start_index:end_index+1])
            start_index = i
        if(string[i] == ';'):
            end_index = i+1
            res.append(string[start_index:end_index])
            start_index = i+1
        else:
            end_index = i
    res.append(string[start_index:end_index+1])
    return res


def xml_formater(input_file, output_file, dictionnaire_code):
    """
    reformatage du fichier pour pouvoir le parser correctement.
    WIP => il est possible que cette fonction ne serve a rien si
    on trouve la solution pour que le parser XML dans python ne crash pas des qu'il rencontre un '&' ou un '#'...
    """
    #recuperation du dictionnaire des codes iso
    dict = dictionnaire_code
    xml = open('XML/'+input_file, 'r')
    #fichier de sortie
    new_xml = open('XML/'+output_file, 'w')
    new_xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")

    print("--------Ouverture de :", input_file, ", création de :", output_file)
    #utilisé pour les tests : permet de stopper l'execution a un seul tour de boucle valide
    i = 0
    first_line = False
    for line in xml:
        #if(i >= 1):
            #break
        if(re.match('.*[^&]&.*[^&]', line)):
            i+=1
            splited_line = split_char_code(line)
            for j in range(len(splited_line)):
                #si le premier caractere d'une sous liste est un '&' alors on est tombé sur un code de caractere spécial à traiter
                if(len(splited_line[j]) > 0):
                    #print("ligne splitée   :",splited_line, "j=", j)
                    if(splited_line[j][0] == '&'):
                        elem = splited_line[j][:-1]
                        #print("elem :",elem)
                        #s'il existe une cle dans le dictionnaire associant ce code avec un char
                        if(elem in dict):
                            #on remplace le code par le char
                            splited_line[j] = dict[elem]
                        #s'il n'est pas dans le dictionnaire, on le supprime => remplce par la chaine vide
                        else:
                        	splited_line[j] = ""
            new_line = ''.join(splited_line)
            #print("ligne originale :",line)
            #print("ligne splitée   :",splited_line)
            #print("ligne modifiée  :", new_line)
            new_xml.write(new_line)
        else:
            if(not(first_line)):
                new_xml.write(line)
        line = xml.readline()
        first_line = False
    new_xml.close()
    xml.close()
    print("--------Fermeture des fichiers", input_file, ", ", output_file)

if __name__ == '__main__':
    dico = create_dict()
    print("----Début du traitement des fichiers XML")
    for i in range(0,7):
        print("--------Traitement du", i+1, "ème fichier xml en cours")
        xml_formater("dblp-0"+str(i)+".xml","newdblp-0"+str(i)+".xml",dico)

    print("-----Traitement des fichiers terminé !")

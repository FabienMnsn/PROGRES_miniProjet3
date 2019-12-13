import json
import re
from xml.dom import minidom

def create_dict():
    """
    fonction qui fabriue un dictionnaire a partir d'un fichier des codes html de carateres spéciaux.
    chaque clé est un code de type &uml et la valeur associée est un caractere
    """
    file = open('table_part2_0.txt', 'r')
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

"""
####USELESS
def position_char(str):
    listS = []
    listE = []
    for i in range(len(str)):
        if(str[i] == '&'):
            listS.append(i)
        if(str[i] == ';'):
            listE.append(i)
    return (listS, listE)
"""

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


def xml_formater(input_file, output_file):
    """
    reformatage du fichier pour pouvoir le parser correctement.
    WIP => il est possible que cette fonction ne serve a rien si
    on trouve la solution pour que le parser XML dans python ne crash pas des qu'il rencontre un '&' ou un '#'...
    """
    #recuperation du dictionnaire des codes iso
    dict = create_dict()
    xml = open('XML/dblp-01.xml')
    #fichier de sortie
    new_xml = open('newdblp-01.xml', 'w')
    new_xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    #utilisé pour les tests : permet de stopper l'execution a un seul tour de boucle valide
    i = 0
    first_line = True
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


if __name__ == '__main__':
    """
    #Tests Samples :
    extract1 = "<author>M. Tamer &Ouml;zsu</author>"
    extract2 = "<title>Die Repr&auml;sentation r&auml;umlichen Wissens und die Behandlung von Einbettungsproblemen mit Quadtreedepiktionen</title>"
    extract3 ="<title>DInG - ein Dom&auml;nen-orientierter Inkrementeller und Integrierter Generator f&uuml;r koh&auml;rente Texte</title>"
    """
    #res_dict = create_dict()
    print("starting xml parse")
    xml_formater()

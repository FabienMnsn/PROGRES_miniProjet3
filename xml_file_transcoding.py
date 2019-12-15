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


def split_string(string):
    """
    split de la string selon les codes de caracteres speciaux
    """
    pattern_end_index = 0
    pattern_start_index = 0
    index = 0
    res = []
    for car in string:
        if(car == '&'):
            for i in range(10):
                if(string[index+i] == ';'):
                    pattern_end_index = index+i
                    res.append(string[index:pattern_end_index])
                    break
                else:
                    res.append(string[index:index+1])

        index+=1




def find_index(split_string, pattern):
    """
    retourne l'index du pattern dans le tableau de string split_string, et -1 en cas d'erreur
    """
    for i in range(len(split_string)+1):
        if(pattern in split_string[i]):
            return i
    return -1


def replace_char_and_join(splited_string, string_elem, dictionnaire, set_not_found):
    """
    remplace le string pattern dans splited _string par le charactere corespondant au motif
    s'il n'existe pas en remplce par le caractere vide
    """
    #safe init
    index = -1
    index = find_index(splited_string, string_elem)
    if(index != -1):
        if(string_elem in dictionnaire):
            splited_string[index] = dictionnaire[string_elem]
        else:
            splited_string[index] = ''
            set_not_found.add(string_elem)
    else:
        print("Error in 'replace_char_and_join' : index value < 0")
        return -1
    return ''.join(splited_string)



def xml_formater(input_file, output_file, dictionnaire_code):
    """
    reformatage du fichier pour pouvoir le parser correctement.
    WIP => il est possible que cette fonction ne serve a rien si
    on trouve la solution pour que le parser XML dans python ne crash pas des qu'il rencontre un '&' ou un '#'...
    """
    #recuperation du dictionnaire des codes iso
    dictio = dictionnaire_code
    xml = open('XML/'+input_file, 'r')
    #fichier de sortie
    new_xml = open('XML/'+output_file, 'w')
    new_xml.write("<?xml version='1.0' encoding='UTF-8'?>\n")

    print("--------Ouverture de :", input_file, ", création de :", output_file)
    for line in xml:
        #on enleve le retour chariot a la fin de la ligne
        line_ = line[:-1]
        #print("ligne originale :",line_)
        contains_special_code = re.search(r"&.*[a-zA-Z0-9^&;]{,6}?;", line_)
        if(contains_special_code != None and len(contains_special_code[0]) > 0):
        #if(contains_special_code and len(contains_special_code) > 0):
            splited_line = split_char_code(line_)
            for elem in splited_line:
                #si  l'element de la liste n'est pas vide
                if(len(elem) > 0):
                    #si le premier caractere d'elem est un '&' alors on est tombé sur un code de caractere spécial à traiter
                    #print("ligne splitée   :",splited_line, "j=", j)
                    if(elem[0] == '&'):
                        #on eneleve le ';' qui est présent dan elem pour lancer la recherche dans le dico
                        elem = elem[:-1]
                        #print("elem :",elem)
                        #s'il existe une cle dans le dictionnaire associant ce code avec un char
                        #if(elem in dict):
                            #on remplace le code par le char
                        #on appel la fct qui retourne une string de la ligne split avec les codes échangés
                        new_line = replace_char_and_join(splited_line, elem, dictio, set_not_found)
                            #splited_line[j] = dict[elem]
                        #s'il n'est pas dans le dictionnaire, on le supprime => remplce par la chaine vide
                        #else:
                            #print("pas trouvé :", elem)
                            #set_not_found.add(elem)
                            #splited_line[j] = ""
            #new_line = ''.join(splited_line)
            #print("ligne originale :",line)
            #print("ligne splitée   :",splited_line)
            #print("ligne modifiée  :", new_line)
            new_xml.write(new_line+"\n")
        else:
            new_xml.write(line_+"\n")
    new_xml.close()
    xml.close()
    print("--------Fermeture des fichiers", input_file, ", ", output_file)


if __name__ == '__main__':
    dico = create_dict()
    set_not_found = set()
    """
    for i in split_char_code("<title>Reduced Complexity Interpolation Architecture for Soft-Decision Reed&#8211;Solomon Decoding.</title>"):
        if(i[0] == '&'):
            print(i)
            i = i[:-1]
            if(i in dico):
                print(dico[i])

    print("----Début du traitement des fichiers XML")
    for i in range(0,1):
        print("--------Traitement du", i+1, "ème fichier xml en cours")
        xml_formater("dblp-0"+str(i)+".xml","newdblp-0"+str(i)+".xml",dico)

    print("-----Traitement des fichiers terminé !")

    print(split_char_code("<title>A 3-10 GHz Ultra Wideband Receiver LNA in 0.13&micro;m CMOS.</title>"))
    print("& in str :",'&' in "<title>A 3-10 GHz Ultra Wideband Receiver LNA in 0.13&micro;m CMOS.</title>")
    #print("&micro" in dico)
    """

    #stri = "<title>Erratum to 'A sample-based method for computing the radiosity inverse matrix' [Computers &amp; Graphics 41 (2014) 1-12].</title>"
    #print(len(re.search(r"&.*[a-zA-Z0-9^&;]{,6}?;", stri)[0]))
    #print(res)
    #print(split_char_code("<title>Erratum to 'A sample-based method for computing the radiosity inverse matrix' [Computers &amp; Graphics 41 (2014) 1-12].</title>"))

    print(split_char_code("<title>Using Kaplan-Meier analysis together with decision tree methods (C&RT, CHAID, QUEST, C4.5 and ID3) in determining recurrence-free survival of breast cancer patients.</title>"))

    #xml_formater("test_parser.xml", "Ptest_parser.xml", dico)


    """
    print("----Début du traitement du fichier XML")
    xml_formater("dblp.xml", "NEWdblp.xml", dico)
    print("----Fin du traitement du fichier XML")

    #print(set_not_found)
    set_file = open('not_found_table.txt', 'w')
    for a in set_not_found:
        set_file.write(a+"\n")
    set_file.close()
    """

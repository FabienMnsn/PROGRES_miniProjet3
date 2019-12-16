import xml.etree.ElementTree as ET


"""
tentative de charger l'extrait du fichier dblp.xml
"""

to_find = "Paul Kocher"

tree = ET.parse('XML/PARSED_extract_dblp.xml')
root = tree.getroot()

res = [0, 0, 0]
other_types = set()

for child in root:
    for grandchild in child:
        #if(grandchild.text == to_find):
        if(child.tag == "article"):
            res[0] += 1
        elif(child.tag == "journal"):
            res[1] += 1
        else:
            #print(child.tag)
            other_types.add(child.tag)



print("[articles, journaux, conferences]")
print(res)

print(other_types)

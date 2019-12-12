import xml.etree.ElementTree as ET
import bottle


#parsing du fichier XML

tree = ET.parse('dblp.xml')
root = tree.getroot()
for child in root:
        print(child)
        break

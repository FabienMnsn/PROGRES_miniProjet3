import xml.etree.ElementTree as ET
import bottle


#parsing du fichier XML

tree = ET.parse('XML/dblp-01.xml')
root = tree.getroot()
for child in root:
        print(child.tag)
        break

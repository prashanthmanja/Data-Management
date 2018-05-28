from lxml import etree
from collections import Counter
import sys

xml_parks = sys.argv[1]
#xml_parks=open('parks.xml')
parser = etree.XMLParser(recover=True)
xmltree = etree.parse(xml_parks, parser=parser)
root = xmltree.getroot()
elemList = []

for elem in xmltree.iter():
    if elem.tag == "LocationType":
        elemList.append(elem.text)

cnt = Counter()
for word in elemList:
    cnt[word] += 1

sorted_location_type = sorted(cnt.items()) 
list_of_lists = [list(elem) for elem in sorted_location_type]

for eachlist in list_of_lists:
    eachlist[1] = str(eachlist[1])
    finalloc = eachlist[0]+" "+eachlist[1]
    print finalloc
    


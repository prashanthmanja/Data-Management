import re
import csv
import sys
import json
import requests
from firebase import firebase

#EDIT THIS LIST WITH YOUR REQUIRED JSON KEY NAMES
fieldnames=['id','name','sponsor','event','venue','place','physical_description','occasion','notes','call_number','keywords','language','date','location','location_type','currency','currency_symbol','status','page_count','dish_count']

def convert(filename):
 csv_filename = filename[0]
 print "Opening CSV file: ",csv_filename
 f=open(csv_filename, 'r')
 csv_reader = csv.DictReader(f,fieldnames)
 json_filename = csv_filename.split(".")[0]+".json"
 print "Saving JSON to file: ",json_filename
 jsonf = open(json_filename,'w')
 next(csv_reader)
 data = json.dumps([r for r in csv_reader])
 jsonf.write(data)
 f.close()
 jsonf.close()

def loadtofirebase():
    url = 'https://inf551a.firebaseio.com/.json'
    data = open('menu-136.json','r')

    for line in data:
            r = requests.put(url, line)
    data.close()

def tokenize():
    with open('menu-136.json', 'r') as f:
        data1 = json.load(f)
    index={}

    print len(data1)
    for i in range(len(data1)):
        for key,value in data1[i].items():
            if key=="event":
                if value != "":
                    if value in index:
                        index[str(value)].append(str(data1[i]['id']))
                    else:
                        index[str(value)]=[str(data1[i]['id'])]
    print index
    dictkeys = index.keys()
    dictkeys = str(dictkeys).split("-")
    str_dictkeys = str(dictkeys)

    nstr = re.sub(r'[?|$|.|!|;|\s+][-]',r'',str_dictkeys)
    nestr = re.sub(r'[^a-zA-Z0-9 ]',r'',nstr)
    neestr= re.sub(r'\s+',r' ',nestr)
    relist_dictkeys = neestr.split(" ")
    flat_list={}
    print ("*******************************************************************************************")
    print relist_dictkeys
    print ("*******************************************************************************************")
    for stri in enumerate(relist_dictkeys):
        newlist = [value for key, value in index.items() if stri[1] in key]
        flat_list[stri[1]]=[item for sublist in newlist for item in sublist]
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print flat_list
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    newdict = {}
    newdict['index'] = flat_list
    print ("******************")
    print newdict
    with open('index.json', 'w') as fp:
        json.dump(newdict, fp,indent=3)

def loadindextofirebase():
    url1 = 'https://inf551a.firebaseio.com/.json'
    data=open('index.json', 'rb')
    requests.patch(url1, data=data)

if __name__=="__main__":
 convert(sys.argv[1:])
 loadtofirebase()
 tokenize()
 loadindextofirebase()

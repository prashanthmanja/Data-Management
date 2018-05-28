from pyspark import SparkContext
from operator import add
import sys
import json


#inputfile="accounts_task2.json"
#outputfile="output_task2b-2.txt"

inputfile=sys.argv[1]
outputfile=sys.argv[2]

sc = SparkContext(appName = 'inf551')
my_RDD_strings = sc.textFile(inputfile)
data = my_RDD_strings.map(json.loads)

def remove_digits(address,account_number):
    address=''.join(i for i in address if not i.isdigit())
    return address,account_number

def Convert(tup, di):
    for a, b in tup:
        di.setdefault(a,[]).append(b)
    return di

data1=data.map(lambda x: (remove_digits(x['address'],x['account_number']))).filter(lambda x: x!=None).collect()
data2=sc.parallelize(data1)
data3 = data2.flatMap(lambda (address,account):[(word,account) for word in address.lower().split()]).collect()
dictionary = {}
indexes=Convert(data3, dictionary)
fp=open(outputfile,"w")
for k, v in indexes.iteritems():
    #print (k+":"+str(v)+"\n")
    fp.write(k+":"+str(v)+"\n")


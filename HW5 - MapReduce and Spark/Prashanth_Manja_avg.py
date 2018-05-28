from pyspark import SparkContext
from pyspark.sql import SQLContext
from operator import add
import sys
import json
#inputfile="accounts_task2.json"
#outputfile="output.txt"

sc = SparkContext(appName = 'inf551')
spark=SQLContext(sc)

inputfile=sys.argv[1]
outputfile=sys.argv[2]


my_RDD_strings = sc.textFile(inputfile)
data = my_RDD_strings.map(json.loads)
def filtered_data(x):
    if x['age']>=20 and x['age']<=30:
        return x
    else:
        return
data_mod = data.filter(filtered_data)
data_mod.count()
data_mod=data_mod.map(lambda x: (x['state'],x['balance']))
rdd_dict=data_mod.countByKey()
total=data_mod.reduceByKey(add).collect()
for i in range(len(total)):
    rdd_dict[total[i][0]]=total[i][1]/float(rdd_dict[total[i][0]])
result=sorted(rdd_dict.items(),key=lambda x:x[0])
fp=open(outputfile,"w+")
for i in result:
    fp.write(i[0]+","+str(i[1])+"\n")

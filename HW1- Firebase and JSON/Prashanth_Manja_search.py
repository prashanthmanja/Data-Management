import collections
import sys
import json
import requests
from firebase import firebase

def search(a,data):
    keyword_list=[]
    keyword_list = a.lower().split(" ")
    result_list=[]
    for word in keyword_list:
        if word in data.keys():
            for i in data.get(word):
                if i not in result_list:
                    result_list.append(i)
        else:
            print "Please enter a valid keyword/s"
    print "ids of all the keywords entered--",result_list


def convert(data):
    if isinstance(data, basestring):
        return str(data).lower()
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data.lower()

if __name__=="__main__":
     url = 'https://inf551a.firebaseio.com/index.json'
     response = requests.get(url)
     data = response.json()
     dict=convert(data)
     search(sys.argv[1],dict)

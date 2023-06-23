#coding: utf-8
import sys
import json
import gzip
import getopt
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import warnings
def read_elastic(es_host, index):
    body = {'query': {'match_all':{}}}
    elastic = Elasticsearch(es_host)
    res = elastic.search(index=index, body=body, scroll='3m',  size=1, request_timeout=60)             
    print(es_host, index, res)
        
if __name__=="__main__":
    read_elastic(sys.argv[1], sys.argv[2])

"""
this script is using the requests module to access es through the REST API they expose
"""

import requests
import json

import time

from common import print_header

# GET /_cat/thread_pool?v # getting general information

# a general query, search logstash everywhere. now, since it's generated by logstash, it returns all
query_all = {
    "query": {
        "query_string":
            {
                "query": "logstash*"
            }
    }
}

print_header(1)
print "First let's just get all"
print "length of log list: %d" % requests.post('http://192.168.99.100:9200/_search',  # using _index and _type is optional
                                               data=json.dumps(query_all)).json()['hits']['total']
print "let's get a sample log line"
for l in requests.post('http://192.168.99.100:9200/_search?size=1',
                       data=json.dumps(query_all)).json()['hits']['hits']:
    print l

print_header(2)
print "now let's search for a specific _index"
index = 'logstash-' + time.strftime(
    "%Y.%m.%d")  # the index generated in subscriber.py by logger.addHandler(logstash.LogstashHandler('elk', 5044, version=1))
print "length of log list: %d" % requests.post('http://192.168.99.100:9200/' + index + '/_search',
                                               data=json.dumps(query_all)).json()['hits']['total']

print_header(3)
print "now let's search for a specific _index and _type"
index = 'logstash-' + time.strftime("%Y.%m.%d")
_type = 'logstash'  # generated the same way
search_url = 'http://192.168.99.100:9200/' + index + '/' + _type + '/_search'
results = requests.post(search_url,
                        data=json.dumps(query_all)).json()['hits']
print "length of log list: %d" % results['total']
print "an example log id: %s" % results['hits'][0]['_id']
print "an example timestamp: %s" % results['hits'][0]['_source']['@timestamp']

print_header(4)
print "now let's change the query"
index = 'logstash-' + time.strftime("%Y.%m.%d")
_type = 'logstash'  # generated the same way
search_url = 'http://192.168.99.100:9200/' + index + '/' + _type + '/_search'

query = {
    "query": {
        "match": {
            "message": "kibana_markable"
        }
    }
}

results = requests.post(search_url,
                        data=json.dumps(query)).json()['hits']
print "length of log list: %d" % results['total']
print "an example log id: %s" % results['hits'][0]['_id']
print "an example timestamp: %s" % results['hits'][0]['_source']['@timestamp']


print_header(5)
print "now let's use terms"
index = 'logstash-' + time.strftime("%Y.%m.%d")
_type = 'logstash'  # generated the same way
search_url = 'http://192.168.99.100:9200/' + index + '/' + _type + '/_search'

query = {
    "query": {
        "terms": {
            "level": ["info"]  # that means that level is in the list. could put there instead: ["debug", "info"]
        }
    }
}

results = requests.post(search_url,
                        data=json.dumps(query)).json()['hits']
print "length of log list: %d" % results['total']
print "an example log id: %s" % results['hits'][1]['_id']
print "an example timestamp: %s" % results['hits'][1]['_source']['@timestamp']


print_header(6)
print "now let's use the AND operator for logical filtering"
index = 'logstash-' + time.strftime("%Y.%m.%d")
_type = 'logstash'  # generated the same way
search_url = 'http://192.168.99.100:9200/' + index + '/' + _type + '/_search?q=message:(kibana_markable AND design)'

results = requests.post(search_url).json()['hits']
print "length of log list: %d" % results['total']
print "an example log id: %s" % results['hits'][1]['_id']
print "an example timestamp: %s" % results['hits'][1]['_source']['@timestamp']


print_header(7)
print "now let's use match_all instead of match query"
index = 'logstash-' + time.strftime("%Y.%m.%d")
_type = 'logstash'  # generated the same way
search_url = 'http://192.168.99.100:9200/' + index + '/' + _type

query = {
    "query": {
        "match": {
            "match_all": {"message": "kibana_markable"}
        }
    }
}
results = requests.post(search_url,
                        data=json.dumps(query)).json()['hits']
print "length of log list: %d" % results['total']
print "an example log id: %s" % results['hits'][1]['_id']
print "an example timestamp: %s" % results['hits'][1]['_source']['@timestamp']



from elasticsearch import Elasticsearch
import requests
# Creating an object of ElasticSearch and checking it's existence
def elasticsearch_connect():
    _es = None
    _es = Elasticsearch(['http://127.0.0.1:9200'])
    if _es.ping:
        print('Connected')
    else:
        print('Could not connect')
    return _es


# Creating an index and specifying the settings and mapping
def create_index(es_db, index_name):
    created = False
    # index settings
    print(index_name)
    create_index = {
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings" : {
        "properties" : {
            "sno" : { "type" : "text" },
            "title": {"type": "text"},
            "author": {"type": "text"},
            "slug": {"type": "text"},
            "content": {"type": "text"}
        }
    }
}

    try:
        if not es_db.indices.exists(index_name):
            es_db.index(index=index_name, ignore=400,
                        body=create_index)  # Used to create an index with the specified settings and mapping.
            print('Created InLdex::%s' % create_index)
            created = True
    except Exception as ex:
        print(ex)
    finally:
        return created

def elastic_client_push(es_db, index_name, record):
    try:
        es_db.index(index=index_name, body=record)     # Adding data to the index

    except Exception as ex:
        print('Error::  %s' % ex)

def search(query, es, index_name):
    results = es.search(index=index_name,body={

        "query": {
            "bool": {
                "should": [
                    {"match": {
                        "title": {
                            'query': query ,
                            "fuzziness": 2,

                        }
                    }
                    }
                ]
            }
        }

    })
    print(results)
    print("Got %d Hits." % results['hits']['total']['value'])
    print(" ")
    print(" ")
    s =[]
    for hit in results['hits']['hits']:
        print(hit['_score'])
        print(hit['_source'])
        print(hit['_id'])
        s.append(hit['_source'])
    return s


def myRequest(queryy):

    es = elasticsearch_connect()  # Creating an object of elasticSearch
    create_index(es, index_name='author')  # Creating an index named captain_america
    return search(queryy, es, 'author')  # Searching a Query

# todo:
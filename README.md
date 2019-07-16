## Docker stuff to get started

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.2.0
```

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.2.0
```

## python libraries

We are using `elasticsearch_dsl`, https://elasticsearch-dsl.readthedocs.io/en/latest/ 

# Basics



## Terminology


### Document

A document is a basic unit of information that can be indexed. For example, you can have a document for a single customer, another document for a single product, and yet another for a single order. This document is expressed in JSON (JavaScript Object Notation) which is a ubiquitous internet data interchange format.



### Shards and Replicas 

An index can potentially store a large amount of data that can exceed the hardware limits of a single node. For example, a single index of a billion documents taking up 1TB of disk space may not fit on the disk of a single node or may be too slow to serve search requests from a single node alone.

To solve this problem, Elasticsearch provides the ability to subdivide your index into multiple pieces called shards. When you create an index, you can simply define the number of shards that you want. Each shard is in itself a fully-functional and independent "index" that can be hosted on any node in the cluster.


Sharding is important for two primary reasons:

- It allows you to horizontally split/scale your content volume
- It allows you to distribute and parallelize operations across shards (potentially on multiple nodes) thus increasing performance/throughput



In a network/cloud environment where failures can be expected anytime, it is very useful and highly recommended to have a failover mechanism in case a shard/node somehow goes offline or disappears for whatever reason. To this end, Elasticsearch allows you to make one or more copies of your index’s shards into what are called replica shards, or replicas for short.

Replication is important for two primary reasons:


- It provides high availability in case a shard/node fails. For this reason, it is important to note that a replica shard is never allocated on the same node as the original/primary shard that it was copied from.
- It allows you to scale out your search volume/throughput since searches can be executed on all replicas in parallel.



To summarize, each index can be split into multiple shards. An index can also be replicated zero (meaning no replicas) or more times. Once replicated, each index will have primary shards (the original shards that were replicated from) and replica shards (the copies of the primary shards).



## Testing if ES is up & running ...

```bash
curl localhost:9200

```

will return something like

```json
{
  "name" : "7f82b6919acb",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "mwT93ju-TXiBwwjlRlS7vQ",
  "version" : {
    "number" : "7.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "508c38a",
    "build_date" : "2019-06-20T15:54:18.811730Z",
    "build_snapshot" : false,
    "lucene_version" : "8.0.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```


## indexing (aka storing documents)

```json
PUT twitter/_doc/1
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
```


Here, `twitter` is the index name, `_doc` is the type.
In previous versions, index was roughly equivalent to a Database and type analogous to a Table.
Since version 6+, this doesn't hold anymore, and types will be eventually become obsolete.



The last part of the `PUT` url, is the doc id. If passed, ES will use this as document identifier, otherwise it will generate ids automatically

If we index a document with the same id, ES will automatically generate versions. 
By default, the most recent version will be returned.


We can obviously create multiple indexes.



A document can be any json object. 
Elasticsearch supports various datatypes: text, integers, floats, doubles, datetimes, geolocations, nexted objects etc




## Retrieving documents


ES is can be considered as a key-value store (which in general is not a good idea).

Retrieving documents is as simple as 

```bash
GET twitter/_doc/0
```

 
 
 
## Searching

```
GET /news/_search?q=title:oaknorth
```


```
GET /news,companies/_search?q=name:oaknorth
```

## Counting 


```
GET /news/_count?q=title:oaknorth
```

```python 

GET /news/_count
{
    "query" : {
        "term" : { "publisher" : "Finacial Times" }
    }
} 

```



## Moving to Python



### elasticsearch_dsl


Create a document class


```python
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save and article
article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

article = Article.get(id=42)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())
```

After running the code

```python
GET /blog/_mapping?pretty

```

will produce something similar to

```python
{
  "blog": {
    "mappings": {
      "properties": {
        "body": {
          "type": "text",
          "analyzer": "snowball"
        },
        "lines": {
          "type": "integer"
        },
        "published_from": {
          "type": "date"
        },
        "tags": {
          "type": "keyword"
        },
        "title": {
          "type": "text",
          "fields": {
            "raw": {
              "type": "keyword"
            }
          },
          "analyzer": "snowball"
        }
      }
    }
  }
}
```
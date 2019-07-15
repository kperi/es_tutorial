from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()



s = Search().using(client).query("match", title="use")
for hit in s:
    print(hit.title)

print( 100*"*")


## do a term query
s = Search().using(client).query("term", title="snowball").execute()
if len(s) == 0:
    print( "query %s is empty" % s.to_dict())
for hit in s:
    print(hit.title)
print( 100*"*")

## do a terms query
s = Search().using(client).query("terms", tags=["test"])
for hit in s:
    print(hit.title)


print( 100*"*")

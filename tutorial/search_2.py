from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q, A

client = Elasticsearch()


s = Search().using(client).query("match", title="dealing")
for hit in s:
    print(hit.meta.id, hit.title, hit.meta.score)

print(100 * "*")


print()
print("multimatch 1 ")

q = Q("multi_match", query="oaknorth bank", fields=["title", "body"])

s = Search().using(client).query(q)
for hit in s:
    print(hit.meta.id, hit.title)

print(100 * "*")


print()
print("multimatch 1 ")

q = Q("multi_match", query="Tesla", fields=["title", "body"])

s = Search().using(client).query(q)
for hit in s:
    print(hit.meta.id, hit.title)

print(100 * "*")

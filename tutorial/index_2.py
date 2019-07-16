from elasticsearch_dsl import Document, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=["localhost"])


class NewsArticle(Document):
    title = Text(analyzer="snowball", fields={"raw": Keyword()})
    body = Text(analyzer="snowball")
    publisher = Keyword()
    tags = Keyword()

    class Index:
        name = "newsarticle"
        settings = {"number_of_shards": 2}


# create the mappings in elasticsearch
NewsArticle.init()


documents = [
    [
        "1",
        "London-based lender OakNorth to double headcount amid deal with Dutch bank",
        "British challenger bank OakNorth is on track to double its headcount after sealing a deal to provide small business loan technology to Dutch ",
        "The Telegraph",
        "Fintech",
    ],
    [
        "2",
        "OAKNORTH LENDS £19.5M TO CARE CONCERN GROUP TO SUPPORT ALPHA REAL CAPITAL OPERATING CARE HOMES",
        "OakNorth Bank has provided a £19.5m loan to Care Concern Group, a UK-based care home operator. Founded in 1991 by Balbir Johal, Care Concern is a family-run business with numerous sites across the UK and a focus on general nursing and dementia care.",
        "Business Leader",
        ["Fintech", "Banking", "SME"],
    ],
    [
        "3",
        "SoftBank-backed lender OakNorth doubles staff, inks deal with X Bank",
        "LONDON (Reuters) - British financial technology firm OakNorth has signed a five-year deal to provide its credit analysis and monitoring platform to D lender X Bank, OakNorth said on Tuesday in its first such agreement to be made public.",
        "Reuters",
        ["Fintech", "Banking"],
    ],
    [
        "4",
        "Tesla drops Standard Range versions of Model S and X",
        "Tesla has discontinued the Standard Range versions of the Model S and Model X, effectively increasing the minimum price of each car by a few thousand dollars, reports Reuters. The company’s online configurator now only lists the Long Range and Performance models of each car as being available to order. ",
        "theverge",
        ["Self Driving Cars", "Tesla"],
    ],
]

for id, title, body, publisher, tags in documents:

    print(id, tags)

    doc = NewsArticle(
        meta={"id": id}, title=title, body=body, publisher=publisher, tags=tags
    )
    doc.save()

# print(connections.get_connection().cluster.health())

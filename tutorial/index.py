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


# create and save and article
article = Article(meta={'id': 43}, title="We are going to be using the Snowball analyser, for analysing text", tags=['test2'])
article.body = ''' 
The Snowball analyzer converts words into language and code set specific stem words.

The Snowball analyzer is similar to the Standard analyzer except that is converts words to stem words.

The Snowball analyzer processes text characters in the following ways:

Converts words to stem word tokens.
Stopwords are not indexed.
Converts alphabetical characters to lower case.
Ignores colons, #, %, $, parentheses, and slashes.
Indexes underscores, hyphens, @, and & symbols when they are part of words or numbers.
Separately indexes numbers and words if numbers appear at the beginning of a word.
Indexes numbers as part of the word if they are within or at the end of the word.
Indexes apostrophes if they are in the middle of a word, but removes them if they are at the beginning or end of a word.
Ignores an apostrophe followed by the letter s at the end of a word.

'''
article.published_from = datetime.now()
article.save()
article = Article.get(id=43)
print(article.is_published())


# Display cluster health
print(connections.get_connection().cluster.health())

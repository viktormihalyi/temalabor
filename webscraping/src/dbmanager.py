import hashlib
from elasticsearch import Elasticsearch


class DbManager:

    ES_INDEX = 'products'
    ES_DOC_TYPE = 'product'

    def __init__(self, elastic_url):
        self.es = Elasticsearch(elastic_url)

    def put(self, item):
        document_id = hashlib.sha256(item['url'].encode('utf-8')).hexdigest()
        self.es.index(index=self.ES_INDEX, doc_type=self.ES_DOC_TYPE, id=document_id, body=item)

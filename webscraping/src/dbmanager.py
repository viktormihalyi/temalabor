import hashlib
from elasticsearch import Elasticsearch


class DbManager:
    """
    Elasticsearch database manager class.
    """

    ES_INDEX = 'products'
    ES_DOC_TYPE = 'product'

    def __init__(self, elastic_url):
        self.es = Elasticsearch(elastic_url)

    def put(self, item):
        """
        Puts an item into the database.
        The "_id" will be a hash of the response url.

        Args:
            item: dictionary that will be saved to Elasticsearch
        """

        document_id = hashlib.sha256(item['url'].encode('utf-8')).hexdigest()
        self.es.index(index=self.ES_INDEX, doc_type=self.ES_DOC_TYPE, id=document_id, body=item)

    def wait_for_connection(self):
        """
        Waits for database connection.
        """

        connected = False
        while not connected:
            connected = self.es.ping()
        return connected


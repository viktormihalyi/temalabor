from scrapy.exceptions import DropItem
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from temalab.items import Product


class HardverAproPipeline(object):
    @staticmethod
    def numbers_from_string(price: str) -> int:
        return int(''.join(c for c in price if c.isdigit()))

    @staticmethod
    def parse_description(desc: BeautifulSoup) -> str:
        return desc.get_text(separator='\n').strip()

    def process_item(self, item: Product, spider):
        item['price'] = self.numbers_from_string(item['price'])
        item['description'] = self.parse_description(item['description'])

        details = item['bs'].select_one('.uad-details')
        intention = details.find_all('div', recursive=False)[2].text
        if "kínál" not in intention:
            raise DropItem('product not for sale')

        return item


class ElasticPipeline(object):
    def __init__(self):
        self.es = None

    def open_spider(self, spider):
        self.es = Elasticsearch('http://localhost:9200')

    def process_item(self, item, spider):
        del item['bs']
        self.es.index(index='products', doc_type='product', body=dict(item))


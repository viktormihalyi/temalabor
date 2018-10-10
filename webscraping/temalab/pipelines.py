from scrapy.exceptions import DropItem
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from temalab.items import Product
import scrapy
import temalab.settings as settings


def numbers_from_string(price: str) -> int:
    return int(''.join(c for c in price if c.isdigit()))


def parse_description(desc: BeautifulSoup) -> str:
    rows = ''.join([str(s).replace('\n', ' ') for s in desc.contents])
    bs_rows = BeautifulSoup(rows, 'html.parser')
    nice_text = bs_rows.get_text(separator='\n')
    return nice_text.strip()


class ProductPipeline(object):
    def process_item(self, item: Product, spider: scrapy.Spider):
        item['price'] = numbers_from_string(item['price'])
        item['description'] = parse_description(item['description'])

        del item['bs']

        return item


class HardverAproPipeline(object):

    SKIPPED_CATEGORIES = ['* boltok, szervizek']

    def process_item(self, item: Product, spider: scrapy.Spider):
        item['price'] = numbers_from_string(item['price'])
        item['description'] = parse_description(item['description'])

        details = item['bs'].select_one('.uad-details')
        del item['bs']

        intention = details.find_all('div', recursive=False)[2].text
        if "kínál" not in intention:
            raise DropItem('product not for sale')

        if item['category'] in self.SKIPPED_CATEGORIES:
            raise DropItem('product in shops/services category')

        return item


class ElasticPipeline(object):
    def __init__(self):
        self.es = None

    def open_spider(self, spider: scrapy.Spider):
        self.es = Elasticsearch(settings.ELASTICSEARCH_URL)

        if not self.es.ping():
            spider.logger.warn('could not connect to elasticsearch')
            self.es = None

    def process_item(self, item, spider: scrapy.Spider):
        if not self.es:
            raise DropItem('not connected to elasticsearch database')

        document_id = item['_id']
        del item['_id']

        if item['title'] is None or item['title'] == "":
            raise DropItem('title missing')

        self.es.index(index='products', doc_type='product', id=document_id, body=dict(item))
        return item

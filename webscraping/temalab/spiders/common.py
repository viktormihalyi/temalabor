import scrapy
from bs4 import BeautifulSoup
from temalab.items import Product
import time

class ParseError(Exception):
    pass


# abstract
class ProductSpider(scrapy.Spider):
    NOT_IMPLEMENTED_METHOD_ERROR = "please implement this method"

    name = '__spider_name'

    # final
    def parse(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        for url in self.get_product_urls(bs):
            yield scrapy.Request(url, callback=self.parse_product)

        yield scrapy.Request(self.get_next_page_url(bs, response), callback=self.parse)

    # abstract
    def get_product_urls(self, bs: BeautifulSoup):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

    # abstract
    def get_next_page_url(self, bs: BeautifulSoup, response):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

    # final
    def parse_product(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        product = {
            '_id': response.url,
            'title': self.get_title(bs),
            'price': self.get_price(bs),
            'url': response.url,
            'site': self.name,
            'description': self.get_description(bs),
            'category': self.get_category(bs),
            'timestamp': time.time(),
            'bs': bs
        }
        return Product(product)

    # abstract
    def get_title(self, bs: BeautifulSoup):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

    # abstract
    def get_price(self, bs: BeautifulSoup):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

    # abstract
    def get_description(self, bs: BeautifulSoup):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

    # abstract
    def get_category(self, bs: BeautifulSoup):
        raise NotImplementedError(self.NOT_IMPLEMENTED_METHOD_ERROR)

from bs4 import BeautifulSoup
import temalab.spiders.common as common
import re


class JofogasSpider(common.ProductSpider):
    name = 'jofogas'
    start_urls = [ 'https://www.jofogas.hu/magyarorszag/muszaki-cikkek-elektronika' ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.ProductPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def get_product_urls(self, bs: BeautifulSoup):
        products = bs.select('.item-title')
        for product in products:
            product_url = product.a.get('href')
            yield product_url

    def get_next_page_url(self, bs: BeautifulSoup, response):
        return bs.select_one('.jofogasicon-right').get('href')

    def get_title(self, bs: BeautifulSoup):
        return bs.select_one('meta[property="og:title"]').get('content')

    def get_price(self, bs: BeautifulSoup):
        price_regex = r'package_price=([0-9]+)'
        match = re.search(price_regex, bs.__str__())
        if match:
            return match.group(1)
        else:
            return None

    def get_description(self, bs: BeautifulSoup):
        return bs.select_one('[itemprop=description]')

    def get_category(self, bs: BeautifulSoup):
        return bs.select_one('[itemprop=category]').select_one('.reParamValue').text

    def get_image_url(self, bs: BeautifulSoup, response):
        return bs.select_one('meta[property="og:image"]').get('content')

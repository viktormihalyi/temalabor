import scrapy
from bs4 import BeautifulSoup
from temalab.items import Product


class HardverAproSpider(scrapy.Spider):
    name = 'hardverapro'
    start_urls = ['https://hardverapro.hu/aprok/hardver/memoria/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.HardverAproPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')
        products = bs.select('[data-uadid]')

        for product in products:
            product_url = product.a.get('href')
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        return Product(
            title=bs.select_one('.uad-content-block').h1.text,
            price=bs.select_one('.uad-details').find_all('div', recursive=False)[0].text,
            url=response.url,
            site=self.name,
            description=bs.select_one('.rtif-content'),
            category='memória',
            bs=bs
        )


import scrapy
from bs4 import BeautifulSoup
from temalab.items import Product


class HasznaltAutoSpider(scrapy.Spider):
    name = 'hasznaltauto'
    pass


class VateraSpider(scrapy.Spider):
    name = 'vatera'
    start_urls = ['https://www.vatera.hu/szamitastechnika/index_c159.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.ProductPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        products = bs.select('a.itemlink')
        for product in products:
            product_url = product.get('href')
            yield scrapy.Request(product_url, callback=self.parse_product)

        next_page_selector = 'img[src="https://img-ssl.vatera.hu/images/search/arw_frw.gif"]'
        next_page = bs.select_one(next_page_selector)
        if next_page:
            next_page_url = next_page.parent.get('href')
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        category = bs.select('[itemprop=title]')[2].text
        price = bs.select_one('.fix-product-price') or bs.select_one('.auction-min-price')

        return Product(
            title=bs.select_one('#pvp-title-subtitle-box-inner2').text,
            price=price.text,
            url=response.url,
            site=self.name,
            description=bs.select_one('#pvp-product-description-box-inner'),
            category=category,
            bs=bs
        )


class JofogasSpiser(scrapy.Spider):
    name = 'jofogas'
    start_urls = [
        # 'https://auto.jofogas.hu/magyarorszag/auto',
        'https://www.jofogas.hu/magyarorszag/muszaki-cikkek-elektronika'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.ProductPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        products = bs.select('.item-title')

        for product in products:
            product_url = product.a.get('href')
            yield scrapy.Request(product_url, callback=self.parse_product)

        next_page = bs.select_one('.jofogasicon-right')
        if next_page:
            next_page_url_abs = next_page.get('href')
            yield scrapy.Request(next_page_url_abs, callback=self.parse)

    def parse_product(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        with open('asd.txt', 'wb') as f:
            f.write(response.body)

        return Product(
            title=bs.select_one('meta[property="og:title"]').content,
            price=bs.select_one('.price-value').text,
            url=response.url,
            site=self.name,
            description=bs.select_one('[itemprop=description]'),
            category=bs.select_one('[itemprop=category]').select_one('.reParamValue').text,
            bs=bs
        )


class HardverAproSpider(scrapy.Spider):
    name = 'hardverapro'
    #start_urls = ['https://hardverapro.hu/aprok/hardver/memoria/index.html']

    start_urls = ['https://hardverapro.hu/aprok/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.HardverAproPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')
        products = bs.select('[data-uadid]')

        # scrape all products in this page
        for product in products:
            product_url = product.a.get('href')
            yield scrapy.Request(product_url, callback=self.parse_product)

        # continue with the next page
        next_page = bs.select_one('a[rel=next]')
        if next_page:
            # create absolute url from a relative one
            next_page_url_abs = response.urljoin(next_page.get('href'))
            yield scrapy.Request(next_page_url_abs, callback=self.parse)

    def parse_product(self, response):
        bs = BeautifulSoup(response.text, 'html.parser')

        category = bs.select('.breadcrumb-item')[3].text.lower()

        return Product(
            title=bs.select_one('.uad-content-block').h1.text,
            price=bs.select_one('.uad-details').find_all('div', recursive=False)[0].text,
            url=response.url,
            site=self.name,
            description=bs.select_one('.rtif-content'),
            category=category,
            bs=bs
        )


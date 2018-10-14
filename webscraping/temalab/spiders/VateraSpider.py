from bs4 import BeautifulSoup
import temalab.spiders.common as common


class VateraSpider(common.ProductSpider):
    name = 'vatera'
    start_urls = ['https://www.vatera.hu/szamitastechnika/index_c159.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.ProductPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def get_product_urls(self, bs: BeautifulSoup):
        products = bs.select('a.itemlink')
        for product in products:
            product_url = product.get('href')
            yield product_url

    def get_next_page_url(self, bs: BeautifulSoup, response):
        next_page_selector = 'img[src="https://img-ssl.vatera.hu/images/search/arw_frw.gif"]'
        next_page = bs.select_one(next_page_selector)
        next_page_url = next_page.parent.get('href')
        return next_page_url

    def get_title(self, bs: BeautifulSoup):
        return bs.select_one('#pvp-title-subtitle-box-inner2').text

    def get_price(self, bs: BeautifulSoup):
        price = bs.select_one('.fix-product-price') or bs.select_one('.auction-min-price')
        return price.text

    def get_description(self, bs: BeautifulSoup):
        return bs.select_one('#pvp-product-description-box-inner')

    def get_category(self, bs: BeautifulSoup):
        return bs.select('[itemprop=title]')[2].text

    def get_image_url(self, bs: BeautifulSoup, response):
        meta_image = bs.select_one('meta[property="og:image"]')
        if meta_image:
            return meta_image.get('content')
        else:
            return None

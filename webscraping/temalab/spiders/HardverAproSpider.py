from bs4 import BeautifulSoup
import temalab.spiders.common as common


class HardverAproSpider(common.ProductSpider):
    name = 'hardverapro'
    start_urls = ['https://hardverapro.hu/aprok/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'temalab.pipelines.HardverAproPipeline': 300,
            'temalab.pipelines.ElasticPipeline': 400,
        }
    }

    def get_product_urls(self, bs: BeautifulSoup):
        products = bs.select('[data-uadid]')
        for product in products:
            product_url = product.a.get('href')
            yield product_url

    def get_next_page_url(self, bs: BeautifulSoup, response):
        next_page = bs.select_one('a[rel=next]')
        next_page_url_abs = response.urljoin(next_page.get('href'))
        return next_page_url_abs

    def get_title(self, bs: BeautifulSoup):
        return bs.select_one('.uad-content-block').h1.text

    def get_price(self, bs: BeautifulSoup):
        return bs.select_one('.uad-details').find_all('div', recursive=False)[0].text

    def get_description(self, bs: BeautifulSoup):
        return bs.select_one('.rtif-content')

    def get_category(self, bs: BeautifulSoup):
        category = bs.select('.breadcrumb-item')[3].text.lower()
        return category

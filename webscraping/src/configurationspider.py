import logging
import scrapy
import time

from tags import *
from selector_parser import parse_selector

logger = logging.getLogger(__name__)


def _get_element_by_tag(list_of_elements, value, tag='name'):
    for el in list_of_elements:
        if el[tag] == value:
            return el


class ConfigurationSpider(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super().__init__(kwargs['config'][TAG_SPIDER_NAME], **kwargs)
        self.config = kwargs['config']

    def start_requests(self):
        for starting_url in self.config['starting_urls']:
            for url in starting_url['urls']:
                yield scrapy.Request(url, callback=self.parse_item_with_method(starting_url['method']))

    def get_method_by_name(self, method_name):
        return _get_element_by_tag(self.config[TAG_METHODS], method_name, tag=TAG_METHOD_NAME)

    def get_collector_by_name(self, collector_name):
        return _get_element_by_tag(self.config[TAG_COLLECTORS], collector_name, tag=TAG_COLLECTOR_NAME)

    def get_selector_by_name(self, selector_name):
        return _get_element_by_tag(self.config[TAG_SELECTORS], selector_name, tag=TAG_SELECTOR_NAME)

    def parse_data_collectors(self, response, called_method):
        for collector_name in called_method[TAG_CALL_COLLECTORS]:
            collector = self.get_collector_by_name(collector_name)

            # collect properties here
            item = {
                'url': response.url,
                'timestamp': time.time(),
                'site': self.name
            }

            # parse each property, and put it back to `item`
            for prop in collector[TAG_PROPERTIES]:
                prop_saved_name = prop[TAG_PROPERTY_NAME]
                prop_type = prop['type']

                prop_selector = self.get_selector_by_name(prop[TAG_SELECTOR])
                prop_value = parse_selector(response, prop_selector, prop_type, one=True)

                item[prop_saved_name] = prop_value

                logger.info('parsed item:')

            item['url'] = response.url
            logger.info(item)

    def follow_links(self, response, called_method):
        for link in called_method[TAG_FOLLOW_LINKS]:

            # selector for the urls
            selector_for_link = self.get_selector_by_name(link[TAG_SELECTOR])

            # this method will be called on the selected urls
            link_method = link[TAG_CALL_METHOD]

            # parse selectors
            actual_urls = parse_selector(response, selector_for_link, 'raw')

            # generate scrapy.Requests for the urls, with the given callback method
            for url in actual_urls:
                yield scrapy.Request(response.urljoin(url),
                                     callback=self.parse_item_with_method(link_method))

    def parse_item_with_method(self, method_name):
        def parse_item(response):
            logger.info('response for method "{}"'.format(method_name))
            called_method = self.get_method_by_name(method_name)

            if TAG_CALL_COLLECTORS in called_method:
                self.parse_data_collectors(response, called_method)

            if TAG_FOLLOW_LINKS in called_method:
                return self.follow_links(response, called_method)

        return parse_item


import logging
import scrapy
import time
from typing import List
from typing import Dict

from tags import *
from selector_parser import parse_selector

logger = logging.getLogger(__name__)


def _get_element_by_tag(list_of_elements: List, value, tag: str):
    for el in list_of_elements:
        if el[tag] == value:
            return el


class ConfigurationSpider(scrapy.Spider):

    # override
    def __init__(self, **kwargs):
        super().__init__(kwargs['config'][TAG_SPIDER_NAME], **kwargs)
        self.config = kwargs['config']
        self.db = self.config['db']

    # override
    def parse(self, response):
        pass

    # override
    def start_requests(self):
        """Returns the starting requests. This is like a main method."""
        for starting_url in self.config['starting_urls']:
            for url in starting_url['urls']:
                yield scrapy.Request(url, callback=self.parse_with_method(starting_url['method']))

    def __get_method_by_name(self, method_name: str):
        """Finds and returns a method given its name."""
        return _get_element_by_tag(self.config[TAG_METHODS], method_name, tag=TAG_METHOD_NAME)

    def __get_collector_by_name(self, collector_name: str):
        """Finds and returns a data collector given its name."""
        return _get_element_by_tag(self.config[TAG_COLLECTORS], collector_name, tag=TAG_COLLECTOR_NAME)

    def parse_data_collectors(self, response, collector_names: List[str]) -> List[Dict]:
        """Execute all collectors on a scrapy.Response object and return the collceted data as items."""
        items = []

        for collector_name in collector_names:
            collector = self.__get_collector_by_name(collector_name)

            # collect properties here
            item = {
                'url': response.url,
                'timestamp': time.time(),
                'site': self.name
            }

            # parse each property, and put it back to `item`
            for prop in collector[TAG_PROPERTIES]:
                prop_selector = prop[TAG_SELECTOR]
                prop_value = parse_selector(response, prop_selector, one=True)

                prop_saved_name = prop[TAG_PROPERTY_NAME]
                item[prop_saved_name] = prop_value

            items.append(item)

        return items

    def follow_links(self, response, follow_links: List[Dict]) -> List[scrapy.Request]:
        """Selects all links on a scrapy.Response, and turns them into scrapy.Request objects."""
        for link in follow_links:

            # urls which will be parsed next
            selector_for_link = link[TAG_SELECTOR]
            actual_urls = parse_selector(response, selector_for_link)

            # this method will be called on the selected urls
            link_method = link[TAG_CALL_METHOD]

            # generate scrapy.Requests for the urls, with the given callback method
            for url in actual_urls:
                yield scrapy.Request(response.urljoin(url),
                                     callback=self.parse_with_method(link_method))

    def parse_with_method(self, method_name: str):
        """Returns a method that will parse a response."""

        def parse_item(response):
            logger.info('response (len: {}) for method "{}"'.format(len(response.text), method_name))
            called_method = self.__get_method_by_name(method_name)

            # methods can collect data and/or follow links

            if TAG_CALL_COLLECTORS in called_method:
                items = self.parse_data_collectors(response, called_method[TAG_CALL_COLLECTORS])
                for item in items:
                    self.db.put(item)

            if TAG_FOLLOW_LINKS in called_method:
                # returning the scrapy.Requests to put them in a queue
                return self.follow_links(response, called_method[TAG_FOLLOW_LINKS])

        return parse_item

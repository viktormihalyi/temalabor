import json
import scrapy
import scrapy.crawler
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
import re

def get_referenced_selectors_in_method(method):
    if 'follow_links' in method:
        follow_links = method['follow_links']
        for link in follow_links:
            yield link['selector']


def get_referenced_collectors_in_method(method):
    if 'data_collectors' in method:
        data_collectors = method['data_collectors']
        for collector in data_collectors:
            yield collector


def get_referenced_selectors_in_collector(collector):
    for prop in collector['properties']:
        if 'selector' in prop:
            yield prop['selector']


def get_referenced_methods(method):
    if 'follow_links' in method:
        called_methods = method['follow_links']
        for link in called_methods:
            yield link['call_method']


def check_ids(possible_ids, referenced_ids, warns_errors, type='name'):
    for ref_id in referenced_ids:
        if ref_id not in possible_ids:
            print('ID_ERROR: {} "{}" is not defined'.format(type, ref_id))
            warns_errors['errors'] += 1

    for id_ in set(possible_ids):
        def_count = possible_ids.count(id_)
        if def_count > 1:
            print('ID_ERROR: {} "{}" is defined multiple times (must be unique)'.format(type, id_, def_count))
            warns_errors['errors'] += 1

    for id_ in possible_ids:
        used_count = referenced_ids.count(id_)
        if used_count == 0:
            print('ID_WARN: {} "{}" is never used'.format(type, id_))
            warns_errors['warnings'] += 1


ENABLED_DEFAULT_VALUE = True

def validate_spider_configuration(spider_config):
    warns_errors = {
        'errors': 0,
        'warnings': 0
    }

    if 'name' not in spider_config:
        print('ERROR: no name defined, exiting')
        return False

    spider_name = spider_config['name']

    enabled = spider_config['enabled'] if 'enabled' in spider_config else ENABLED_DEFAULT_VALUE

    # skip validation if spider is disabled
    if not enabled:
        print('INFO: spider "{}" is disabled, not validating'.format(spider_name))
        return
    else:
        print('DEBUG: validating spider "{}"'.format(spider_name))

    if 'starting_urls' not in spider_config:
        print('ERROR: no starting url defined, exiting')
        return False

    # collect referenced names here
    selectors_referenced = []
    collectors_referenced = []
    methods_referenced = []

    for starting in spider_config['starting_urls']:
        if 'method' not in starting:
            print('ERROR: no method defined in starting_urls, exiting')
            return False
        else:
            methods_referenced.append(starting['method'])

    # collect referenced names in methods
    if 'methods' not in spider_config:
        print('ERROR: no methods defined')
        warns_errors['errors'] += 1
    else:
        for method in spider_config['methods']:
            for ref_selector in get_referenced_selectors_in_method(method):
                selectors_referenced.append(ref_selector)

            for ref_collector in get_referenced_collectors_in_method(method):
                collectors_referenced.append(ref_collector)

            for ref_method in get_referenced_methods(method):
                methods_referenced.append(ref_method)

    # collect referenced names in data collectors
    if 'data_collectors' not in spider_config:
        print('WARN: no data collectors defined')
    else:
        for collector in spider_config['data_collectors']:
            for ref_selector in get_referenced_selectors_in_collector(collector):
                selectors_referenced.append(ref_selector)

    # defined selector, method and data collector names
    selector_names = [sel['name'] for sel in spider_config['selectors']]
    collector_names = [coll['name'] for coll in spider_config['data_collectors']]
    method_names = [method['name'] for method in spider_config['methods']]

    check_ids(selector_names, selectors_referenced, warns_errors, type='selector')
    check_ids(collector_names, collectors_referenced, warns_errors, type='data collector')
    check_ids(method_names, methods_referenced, warns_errors, type='method')

    if warns_errors['errors'] > 0:
        print('INFO: {} errors found'.format(warns_errors['errors']))

    if warns_errors['warnings'] > 0:
        print('INFO: {} warnings found'.format(warns_errors['warnings']))

    return warns_errors['errors'] == 0


def get_element_by_name(list_of_elements, name):
    for el in list_of_elements:
        if el['name'] == name:
            return el


class ConfigurationSpider(scrapy.Spider):
    name = 'asd'

    def __init__(self, name=None, **kwargs):
        super().__init__(kwargs['config']['name'], **kwargs)
        self.config = kwargs['config']

    def start_requests(self):
        print(self.config)
        for starting_url in self.config['starting_urls']:
            for url in starting_url['urls']:
                yield scrapy.Request(url, callback=self.parse_item(starting_url['method']))

    def parse_item(self, method_name):
        def inner_parse(response):
            print(get_element_by_name(self.config['methods'], method_name))
            print('len is', len(response.text))
            pass

        return inner_parse


if __name__ == '__main__':
    with open('spiders.json') as f:
        spider_config = json.load(f)

    success = validate_spider_configuration(spider_config)
    if not success:
        exit()

    runner = scrapy.crawler.CrawlerProcess(get_project_settings())
    runner.crawl(ConfigurationSpider, config=spider_config)
    runner.start()





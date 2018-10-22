import os
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from config_validator import validate_spider_configuration
from configurationspider import ConfigurationSpider


if __name__ == '__main__':
    configure_logging()

    with open(os.path.join('spiders', 'spiders.json')) as f:
        spider_config = json.load(f)

    success = validate_spider_configuration(spider_config)
    if not success:
        exit()

    runner = CrawlerProcess(get_project_settings())
    runner.crawl(ConfigurationSpider, config=spider_config)
    runner.start()



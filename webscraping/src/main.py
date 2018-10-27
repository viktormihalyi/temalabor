import os
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import scrapy.utils.project

from config_validator import validate_spider_configuration
from configurationspider import ConfigurationSpider


if __name__ == '__main__':
    configure_logging()

    # all config files must be in the 'spiders' directory
    spider_files = os.listdir('spiders')

    runner = CrawlerProcess(get_project_settings())

    for spider_file in spider_files:
        with open(os.path.join('spiders', spider_file)) as f:
            spider_config = json.load(f)

        # terminate if the validation fails
        success = validate_spider_configuration(spider_config)
        if not success:
            exit()

        runner.crawl(ConfigurationSpider, config=spider_config)

    runner.start()

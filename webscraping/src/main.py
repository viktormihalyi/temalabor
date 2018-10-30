import os
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import scrapy.utils.project

from config_validator import validate_spider_configuration
from configurationspider import ConfigurationSpider

from dbmanager import DbManager

if __name__ == '__main__':
    configure_logging()

    # src/settings.py
    project_settings = get_project_settings()

    # all config files must be in the 'spiders' directory
    spider_files = os.listdir('spiders')

    # create db manager
    db = DbManager(elastic_url=project_settings.get('ELASTICSEARCH_URL'))

    runner = CrawlerProcess(settings=project_settings)

    for spider_file in spider_files:
        with open(os.path.join('spiders', spider_file)) as f:
            spider_config = json.load(f)

        spider_config['db'] = db

        # terminate if the validation fails
        success = validate_spider_configuration(spider_config)
        if not success:
            exit()

        runner.crawl(ConfigurationSpider, config=spider_config)

    runner.start()

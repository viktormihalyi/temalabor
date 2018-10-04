import scrapy


class Product(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()

    bs = scrapy.Field()


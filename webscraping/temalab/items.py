import scrapy


class Product(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    timestamp = scrapy.Field()
    image_url = scrapy.Field()

    bs = scrapy.Field()


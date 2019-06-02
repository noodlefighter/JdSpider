
import scrapy

class JDItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    color = scrapy.Field()
    ratio = scrapy.Field()
    resolution = scrapy.Field()
    refresh_rate = scrapy.Field()
    luminance = scrapy.Field()
    
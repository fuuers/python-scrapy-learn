# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrtestItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    path = scrapy.Field()

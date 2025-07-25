# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TermediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    title = scrapy.Field()
    license = scrapy.Field()

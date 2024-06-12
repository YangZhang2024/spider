# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PicItem(scrapy.Item):
    # define the fields for your item here like:
    pic_set_name = scrapy.Field()
    file_name = scrapy.Field()
    b64_content = scrapy.Field()
    pass

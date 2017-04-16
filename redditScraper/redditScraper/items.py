# -*- coding: utf-8 -*-
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class RedditscraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DataPicItem(Item):
    title=Field()
    pass

class ImageItem(Item):
    image_urls = Field()
    images = Field()
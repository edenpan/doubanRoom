# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class DoubanroomItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class RoomInfoItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    startTime = scrapy.Field()
    startNumTime = scrapy.Field()
    lastUpTime = scrapy.Field()
    ownerId = scrapy.Field()
    ownerUrl = scrapy.Field()
    ownerName = scrapy.Field()
    upDate = scrapy.Field()
    upNumDate = scrapy.Field()
    src = scrapy.Field()

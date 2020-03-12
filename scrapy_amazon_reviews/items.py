# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonReview(scrapy.Item):
   # define the fields for your item here like:
   id = scrapy.Field()
   date = scrapy.Field()
   username = scrapy.Field()
   badge = scrapy.Field()
   stars = scrapy.Field()
   model = scrapy.Field()
   variation = scrapy.Field()
   upvotes = scrapy.Field()
   comments = scrapy.Field()
   replied = scrapy.Field()
   title = scrapy.Field()
   url = scrapy.Field()
   reply = scrapy.Field()
   body = scrapy.Field()
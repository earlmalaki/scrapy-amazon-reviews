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
   stars = scrapy.Field()
   model = scrapy.Field()
   codename = scrapy.Field()
   program = scrapy.Field()
   purchaseType = scrapy.Field()
   title = scrapy.Field()
   body = scrapy.Field()
   url = scrapy.Field()
   upvotes = scrapy.Field()
   comments = scrapy.Field()
   LXKresponded = scrapy.Field()
   reply = scrapy.Field()
   preprocessed_body = scrapy.Field()
   
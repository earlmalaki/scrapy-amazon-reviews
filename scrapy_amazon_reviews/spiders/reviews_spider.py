# -*- coding: utf-8 -*-
 
# Importing Scrapy Library
import scrapy

# Import auxilliary files
import scraper_constants as constants
import scraper_products as products_source

import sys
 
# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
    # Spider name
    name = 'amazon_reviews'

    def start_requests(self):
        urls = []

        page_num = 1
        for product in products_source.get_products():
            print(product)
            url = constants.PR_URL_BASE + product['asin'] + constants.PR_URL_PARAMS + constants.PR_URL_PAGE + str(page_num) + constants.PR_URL_SELLERID + constants.PR_SELLERID_LXK
            
            urls.append(url)
        print (urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # Defining a Scrapy parser
    def parse(self, response):
            data = response.css('#cm_cr-review_list')
             
            # Collecting product star ratings
            star_rating = data.css('.review-rating')
             
            # Collecting user reviews
            comments = data.css('.review-text')
            count = 0
             
            # Combining the results
            for review in star_rating:
                yield{'stars': ''.join(review.xpath('.//text()').extract()),
                      'comment': ''.join(comments[count].xpath(".//text()").extract())
                     }
                count=count+1
# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy
from scrapy_amazon_reviews.items import AmazonReview

import sys
import json
import requests
import html
from bs4 import BeautifulSoup

# Import auxilliary files
import scraper_constants as constants
import scraper_products as products_source

# Creating a new class to implement Spider
class AmazonReviewsSpider(scrapy.Spider):
  # Spider name
  name = 'amazon_reviews'
  allowed_domains = ['www.amazon.com']
  
  def start_requests(self):
    # yield requests for all starting urls
    # starting urls are page 1 of product review page for each product
    # pass product info (ASIN and Model) to parse method via meta attr
    for product in products_source.get_products():
      url = constants.PR_URL_BASE + product['asin'] + constants.PR_URL_PARAMS
      yield scrapy.Request(url=url,callback=self.parse,meta=product)

  # Defining a Scrapy parser
  def parse(self, response):
    # extract passed data (product)
    product = response.meta

    # Get page section that contains the reviews
    # Then get selector for all reviews in the page
    reviews_data = response.css('#cm_cr-review_list')
    reviews = reviews_data.css('div[data-hook="review"]')

    for review in reviews:
      id = review.css('div[data-hook="review"]::attr(id)').get()
      date = review.css('span[data-hook="review-date"]::text').get().strip('\n ').split(" on ")[1]
      username = review.css('.a-profile-name::text').get().strip('\n ')
      rating = review.css('i[data-hook="review-star-rating"] > .a-icon-alt::text').get().strip('\n ')[0]
      variation = review.css('a[data-hook="format-strip"]::text').get(default="N/A").strip('\n ')

      # Verified
      badgeVer = review.css('span[data-hook="avp-badge"]::text').get()
      # Vine
      badgeVine = review.css('.a-color-success.a-text-bold::text').get()
      if (badgeVer is None and badgeVine is None):
        badge = constants.BADGE_NOT_VER
      elif (badgeVer is not None):
        badge = constants.BADGE_VER
      elif (badgeVine is not None):
        badge = constants.BADGE_VINE

      upvote = review.css('span[data-hook="helpful-vote-statement"]::text').get(default="0").strip('\n ').split(' ')[0]
      if (upvote == constants.AMZN_DEF_UPVOTE_ONE):
          upvote = 1
      else:
          upvote = int(upvote)
      
      title = review.css('a[data-hook="review-title"] > span::text').get().strip('\n ')
      body = review.css('span[data-hook="review-body"] > span').xpath('normalize-space(.)').get().strip('\n ')
      comments_count = review.css('.review-comment-total.aok-hidden::text').get().strip('\n ')

      # Get comments via scrapy AJAX request
      # payload = constants.AMZ_AJAX_COMMENTS_PAYLOAD
      # payload['asin'] = "B07T4LGDGQ"
      # payload['reviewId'] = id
      # if (int(comments) != 0):
      #   yield scrapy.Request(constants.AMZ_AJAX_COMMENTS_URL,
      #                         callback=self.parse_comments,
      #                         method="POST",
      #                         # headers=constants.AMZ_AJAX_COMMENTS_HEADERS,
      #                         body=json.dumps(payload))
      
      if (int(comments_count) == 0):
        lxk_rep = {'replied': 'No',
                  'reply': ""}
      else:
          lxk_rep = self.get_lxk_reply(product['asin'], id)

      url = constants.CR_URL_BASE + id + constants.CR_URL_PARAMS + product['asin']
      
      item = AmazonReview()
      item['id'] = id
      item['date'] = date
      item['username'] = username
      item['badge'] = badge
      item['stars'] = rating
      item['model'] = product['model']
      item['variation'] = variation      
      item['upvotes'] = upvote
      item['comments'] = comments_count
      item['replied'] = lxk_rep['replied']
      item['title'] = title
      item['body'] = body
      item['reply'] = lxk_rep['reply']
      item['url'] = url
      yield item

    # Get the URL stored in the next page button's href attribute
    # Then follow each page and the next page until exhausted
    next_page = reviews_data.css('div[data-hook="pagination-bar"]').css('.a-last > a::attr(href)').get()
    if next_page is not None:
      yield response.follow(next_page, callback=self.parse, meta=product)


  def get_lxk_reply(self, asin, id):
    with requests.Session() as s:
      # Post AJAX request to get HTML for comments
      # Strip spaces and newlines
      # Convert to list on "&&&"
      payload = constants.AMZ_AJAX_COMMENTS_PAYLOAD
      payload['asin'] = asin
      payload['reviewId'] = id

      response = s.post(constants.AMZ_AJAX_COMMENTS_URL, payload).text.strip(' \n ').split("&&&")
      
      # Get list of comments and iterate through it
      for data in response[1:]:
        try:
          # Get HTML text body
          data = data.split('","')[2]
          # Unescape quotes
          unescaped = html.unescape(data)[:-2]
          # Unescape \
          clean = unescaped.replace('\\"', '"')
        except Exception as e:
          # The 3rd element is not a comment
          # Must break from execution for this useless element
          break
        
        soup = BeautifulSoup(clean, "lxml")
        try:
          author = soup.find("a", {"data-hook":"review-author"}).get_text().strip(' \n ')

          if (author == constants.LXK_AMZN_ACCNT):
            reply_text = soup.find("span", {"class":"review-comment-text"}).get_text().strip('\n ')
            return {'replied': 'Yes',
                    'reply': reply_text}
        except Exception as e:
          pass
    return {'replied': 'No',
            'reply': ""}
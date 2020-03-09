# -*- coding: utf-8 -*-

# Importing Scrapy Library
import scrapy
from scrapy.http import FormRequest

# Import auxilliary files
import scraper_constants as constants
import scraper_products as products_source

import sys

# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
  # Spider name
  name = 'amazon_reviews'
  allowed_domains = ['www.amazon.com']
  
  def start_requests(self):
    urls = []

    # Make a list of all starting URLs
    # Starting URLs are all page 1 of all product reviews' page
    page_num = 1
    for product in products_source.get_products():
      urls.append(
        constants.PR_URL_BASE +
        product['asin'] +
        constants.PR_URL_PARAMS +
        constants.PR_URL_PAGE +
        str(page_num) +
        constants.PR_URL_SELLERID +
        constants.PR_SELLERID_LXK
        )

    # Give Scrapy a Request foreach URL
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  # Defining a Scrapy parser
  def parse(self, response):

    # Get page section that contains the reviews
    reviews_data = response.css('#cm_cr-review_list')
    # Then get selector for all reviews in the page
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

      comments = review.css('.review-comment-total.aok-hidden::text').get().strip('\n ')

      # Get comments
      payload = constants.AMZ_AJAX_COMMENTS_PAYLOAD
      payload['asin'] = "B07T4LGDGQ"
      payload['reviewId'] = id
      # yield FormRequest(url=constants.AMZ_AJAX_COMMENTS_URL,
      #                   formdata=payload,
      #                   callback=self.parse_comments)
      # yield scrapy.Request(
      #   url=constants.AMZ_AJAX_COMMENTS_URL,
      #   callback=self.parse_comments,
      #   method="POST",
      #   headers=constants.AMZ_AJAX_COMMENTS_HEADERS,
      #   meta=payload
      # )
      

      yield {
        constants.ID: id,
        constants.DATE: date,
        constants.USERNAME: username,
        constants.RATING: rating,
        # constants.MODEL: ,
        constants.VARIATION: variation,
        constants.BADGE: badge,
        constants.UPVOTE: upvote,
        constants.COMMENTS: comments,
        constants.TITLE: title,
        constants.BODY: body
        # constants.LXK_REPLIED: ,
        # constants.LXK_REPLY: 
      }

    # Get the URL stored in the next page button's href attribute
    # Then follow each page and the next page until exhausted
    next_page = reviews_data.css('div[data-hook="pagination-bar"]').css('.a-last > a::attr(href)').get()
    if next_page is not None:
      yield response.follow(next_page, callback=self.parse)

  def parse_comments(self, response):
    from scrapy.shell import inspect_response
    inspect_response(response, self)
    # print(response.body)


# Returns the URL for each specific customer review
def get_customer_review_URL(rev_ID, ASIN):
  url = constants.CR_URL_BASE + rev_ID + constants.CR_URL_PARAMS + ASIN
  return url
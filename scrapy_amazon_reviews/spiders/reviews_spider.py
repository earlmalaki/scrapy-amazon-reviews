########################################
# Author : Earl Timothy D. Malaki
# User Experience Designer
# Plaza 2 6th Floor C'10 6
# Lexmark Research and Development Cebu
########################################
"""
The main spider for the project.
Below is a high level view of the flow:
- get a list of products from product_list.py
- Scrapy requests the page for each product
- Extract data for each page
- Use utility.py for computation and manipulations
- Output .csv files to amazon_reviews
"""
########################################

# Importing libraries
import scrapy
from scrapy_amazon_reviews.items import AmazonReview

import requests
import html
from bs4 import BeautifulSoup

# Import helper files
from scrapy_amazon_reviews import utility
from scrapy_amazon_reviews import product_list

# Creating a new class to implement Spider
class AmazonReviewsSpider(scrapy.Spider):
    # Spider name
    name = "amazon_reviews"
    allowed_domains = ["www.amazon.com"]

    def start_requests(self):
        # yield requests for all starting urls
        # starting urls are page 1 of product review page for each product
        # pass product info (ASIN and Model) to parse method via meta attr
        for product in product_list.get_products():
            url = utility.PR_URL_BASE + product["asin"] + utility.PR_URL_PARAMS + "1"
            yield scrapy.Request(url=url, callback=self.parse, meta=product)

    # Defining a Scrapy parser
    def parse(self, response):
        # extract passed data (product)
        product = response.meta

        # Get number of reviews
        # Calculate number of pages based on number of reviews
        # Yield URLs for all pages
        numberOfReviews = response.css(
            'span[data-hook="cr-filter-info-review-count"]'
        ).get()
        if numberOfReviews is not None:
            numberOfReviews = int(numberOfReviews.strip("\n ").split()[-2])
            if numberOfReviews > 10:
                numberOfPages = numberOfReviews / 10
                if not numberOfPages.is_integer():
                    numberOfPages += 1
                numberOfPages = int(numberOfPages) + 1

                for x in range(2, numberOfPages):
                    url = (
                        utility.PR_URL_BASE
                        + product["asin"]
                        + utility.PR_URL_PARAMS
                        + str(x)
                    )
                    yield scrapy.Request(url=url, callback=self.parse, meta=product)

        # Get page section that contains the reviews
        # Then get selector for all reviews in the page
        reviews_data = response.css("#cm_cr-review_list")
        reviews = reviews_data.css('div[data-hook="review"]')

        for review in reviews:
            id = review.css('div[data-hook="review"]::attr(id)').get()
            date = (
                review.css('span[data-hook="review-date"]::text')
                .get()
                .strip("\n ")
                .split(" on ")[1]
            )
            username = review.css(".a-profile-name::text").get().strip("\n ")
            rating = (
                review.css('i[data-hook="review-star-rating"] > .a-icon-alt::text')
                .get()
                .strip("\n ")[0]
            )
            # variation = review.css('a[data-hook="format-strip"]::text').get(default="N/A").strip('\n ')

            [program, codename] = utility.get_program_codename(product["model"])

            # Verified
            badgeVer = review.css('span[data-hook="avp-badge"]::text').get()
            # Vine
            badgeVine = review.css(".a-color-success.a-text-bold::text").get()
            if badgeVer is None and badgeVine is None:
                badge = utility.BADGE_NOT_VER
            elif badgeVer is not None:
                badge = utility.BADGE_VER
            elif badgeVine is not None:
                badge = utility.BADGE_VINE

            upvote = (
                review.css('span[data-hook="helpful-vote-statement"]::text')
                .get(default="0")
                .strip("\n ")
                .split(" ")[0]
            )
            if upvote == utility.AMZN_DEF_UPVOTE_ONE:
                upvote = 1
            else:
                upvote = int(upvote)

            title = (
                review.css('a[data-hook="review-title"] > span::text')
                .get()
                .strip("\n ")
            )
            body = (
                review.css('span[data-hook="review-body"] > span')
                .xpath("normalize-space(.)")
                .get()
                .strip("\n ")
            )
            comments_count = (
                review.css(".review-comment-total.aok-hidden::text").get().strip("\n ")
            )

            # Get comments via scrapy AJAX request
            # payload = utility.AMZ_AJAX_COMMENTS_PAYLOAD
            # payload['asin'] = "B07T4LGDGQ"
            # payload['reviewId'] = id
            # if (int(comments) != 0):
            #   yield scrapy.Request(utility.AMZ_AJAX_COMMENTS_URL,
            #                         callback=self.parse_comments,
            #                         method="POST",
            #                         # headers=utility.AMZ_AJAX_COMMENTS_HEADERS,
            #                         body=json.dumps(payload))

            if int(comments_count) == 0:
                lxk_rep = {"replied": "No", "reply": ""}
            else:
                lxk_rep = self.get_lxk_reply(product["asin"], id)
                # lxk_rep = {'replied': 'No','reply': ""}   # Filler

            url = utility.CR_URL_BASE + id + utility.CR_URL_PARAMS + product["asin"]

            item = AmazonReview()
            item["id"] = id
            item["date"] = date
            item["username"] = username
            item["stars"] = rating
            item["model"] = product["model"]
            item["codename"] = codename
            item["program"] = program
            item["purchaseType"] = badge
            item["title"] = title
            item["body"] = body
            item["url"] = url
            item["upvotes"] = upvote
            item["comments"] = comments_count
            item["LXKresponded"] = lxk_rep["replied"]
            item["reply"] = lxk_rep["reply"]
            item["preprocessed_body"] = utility.preprocess(body)
            yield item

    def get_lxk_reply(self, asin, id):
        with requests.Session() as s:
            # Post AJAX request to get HTML for comments
            # Strip spaces and newlines
            # Convert to list on "&&&"
            payload = utility.AMZ_AJAX_COMMENTS_PAYLOAD
            payload["asin"] = asin
            payload["reviewId"] = id

            response = (
                s.post(utility.AMZ_AJAX_COMMENTS_URL, payload)
                .text.strip(" \n ")
                .split("&&&")
            )

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
                    author = (
                        soup.find("a", {"data-hook": "review-author"})
                        .get_text()
                        .strip(" \n ")
                    )

                    if author == utility.LXK_AMZN_ACCNT:
                        reply_text = (
                            soup.find("span", {"class": "review-comment-text"})
                            .get_text()
                            .strip("\n ")
                        )
                        return {"replied": "Yes", "reply": reply_text}
                except Exception as e:
                    pass
        return {"replied": "No", "reply": ""}

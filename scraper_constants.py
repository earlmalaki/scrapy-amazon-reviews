# Constant values for product reviews URL constructor
# https://www.amazon.com/product-reviews/ASIN?sortBy=recent&pageNumber=1&m=SELLERID
# *asin, page number, seller id*
PR_URL_BASE = "https://www.amazon.com/product-reviews/"
PR_URL_PARAMS = "?ie=UTF8&reviewerType=all_reviews&sortBy=helpful&"
PR_URL_PAGE = "pageNumber="
PR_URL_SELLERID = '&m='
PR_SELLERID_LXK = '2529788011'
# To get a seller's unique page for a product,
# include both ASIN and sellerID
# https://www.amazon.com/product-reviews/ASIN?sortBy=recent&pageNumber=1&m=SELLERID
# https://www.amazon.com/product-reviews/B07F21DSM8?sortBy=recent&pageNumber=1&m=2529788011


# Constant values for particular customer review URL constructor
# https://www.amazon.com/gp/customer-reviews/REV_ID?ie=UTF8&ASIN=ASIN
# *rev_id, asin*
CR_URL_BASE = "https://www.amazon.com/gp/customer-reviews/"
CR_URL_PARAMS = "?ie=UTF8&ASIN="
# To get a single review,
# https://www.amazon.com/gp/customer-reviews/REV_ID?ie=UTF8&ASIN=ASIN
# https://www.amazon.com/gp/customer-reviews/R1LVMAR6YBYF7X?ASIN=B07T4LGDGQ


# Constant values for script checking
ID = "id"
DATE = "date"
USERNAME = "username"
RATING = "stars"
MODEL = "model"
BADGE = "badge"
TITLE = "title"
BODY = "body"
UPVOTE = "upvotes"
COMMENTS = "comments"
LXK_REPLIED = "replied"
LXK_REPLY = "reply"
URL = "url"
VARIATION = "variation"

OUTPUT_NAME_PREFIX = "Scraper_AmznRvws_"
OUTPUT_NAME_POSTFIX = ".csv"
####

# Amazon Default Values
# Used for checking each review's data points
AMZN_DEF_UPVOTE_ONE = "One"
AMZN_DEF_OFFICIAL_COMMENT = "The manufacturer commented on the review below"

BADGE_NOT_VER = "Unverified"
BADGE_VER = "Verified Purchase"
BADGE_VINE = "Vine Customer"

LXK_AMZN_ACCNT = "Lexmark Support"

# AJAX Constants for opening comments
AMZ_AJAX_COMMENTS_URL = "https://www.amazon.com/hz/reviews-render/ajax/comment/get/ref=cm_cr_arp_d_cmt_opn"
AMZ_AJAX_COMMENTS_HEADERS = {
    "accept": "text/html,*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,fil;q=0.8",
    "content-length": "128",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://www.amazon.com",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
AMZ_AJAX_COMMENTS_PAYLOAD = {
    'sortCommentsBy': 'newest',
    'offset': 0,
    'count': 35,
    # 'pageIteration': 0,
    'asin': "",
    'reviewId': ""
    # 'nextPageToken': '',
    # 'scope': 'reviewsAjax1'
}

# AJAX Constants for accessing more comments
AMZ_AJAX_MORE_COMMENTS_URL = "https://www.amazon.com/hz/reviews-render/ajax/comment/get/ref=cm_cr_getc_d_cmt_btn"
AMZ_AJAX_MORE_COMMENTS_HEADERS = {
    "accept": "text/html,*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,fil;q=0.8",
    "content-length": "160",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://www.amazon.com",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
AMZ_AJAX_COMMENTS_PAYLOAD = {
    'sortCommentsBy': 'newest',
    'offset': 5,
    'count': 25,
    'asin': "",
    'reviewId': ""
}
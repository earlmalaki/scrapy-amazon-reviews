# URL for Amazon Review Page for a prodcut
PR_URL_BASE = "https://www.amazon.com/product-reviews/"
PR_URL_PARAMS = "?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1&m=2529788011"
# Example: https://www.amazon.com/product-reviews/B07F21DSM8?sortBy=recent&pageNumber=1&m=2529788011
# Vars -> ASIN (B07F21DSM8), Page (1), Lexmark Amazon Seller ID (2529788011)

# URL for Amazon Review Page for a customer review
CR_URL_BASE = "https://www.amazon.com/gp/customer-reviews/"
CR_URL_PARAMS = "?ie=UTF8&ASIN="
# Example: https://www.amazon.com/gp/customer-reviews/R1LVMAR6YBYF7X?ASIN=B07T4LGDGQ
# Vars -> Review ID (R1LVMAR6YBYF7X), ASIN (B07T4LGDGQ)

OUTPUT_NAME_PREFIX = "Scrapy_AmazonReviews_"
OUTPUT_NAME_POSTFIX = ".csv"

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
    # "content-length": "128",
    # "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    # "origin": "https://www.amazon.com",
    # "sec-fetch-site": "same-origin",
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    # "x-requested-with": "XMLHttpRequest"
}
AMZ_AJAX_COMMENTS_PAYLOAD = {
    'sortCommentsBy': 'newest',
    'offset': 0,
    'count': 35,
    'asin': "",
    'reviewId': ""
}

# AJAX Constants for accessing more comments
# AMZ_AJAX_MORE_COMMENTS_URL = "https://www.amazon.com/hz/reviews-render/ajax/comment/get/ref=cm_cr_getc_d_cmt_btn"
# AMZ_AJAX_MORE_COMMENTS_HEADERS = {
#     "accept": "text/html,*/*",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "en-US,en;q=0.9,fil;q=0.8",
#     "content-length": "160",
#     "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
#     "origin": "https://www.amazon.com",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
#     "x-requested-with": "XMLHttpRequest"
# }
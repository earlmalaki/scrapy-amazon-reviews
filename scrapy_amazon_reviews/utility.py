########################################
# Authors:
# Earl Malaki
# Joy Trocio
########################################
# - utility file
# - contains a mix of utiliy static constants, utility methods
# - also contains product map object. Used to map models <-> codename <-> program.
# - for more information, kindly refer to the source documentation.
########################################




# Text preprocessing utility

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer, SnowballStemmer

# Converts a string of words into tokens
def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

# Converts tokens to lowercase
def lowercase(tokens):
    return [w.lower() for w in tokens]

# Remove punctuations from tokens
def remove_punctuations(tokens):
    table = str.maketrans("", "", string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    return [word for word in stripped if word.isalpha()]

# Remove stopwords
def remove_stopwords(tokens):
    stop_words = set(stopwords.words("english"))
    return [w for w in tokens if not w in stop_words]

# Stem
def stem(tokens):
    porter = PorterStemmer()
    return [porter.stem(word) for word in tokens]

# Stem and lemmatize
def lemmatize_stemming(tokens):
    stemmer = SnowballStemmer("english")
    return [
        stemmer.stem(WordNetLemmatizer().lemmatize(word, pos="v")) for word in tokens
    ]

def preprocess(text):
    tokens = tokenize(text)
    tokens = lowercase(tokens)
    tokens = remove_punctuations(tokens)
    tokens = remove_stopwords(tokens)
    # tokens = stem(tokens)
    # tokens = lemmatize_stemming(tokens)
    # return tokens
    temp = " "
    return temp.join(tokens)





# Contains constant values and utility variables
# URL for the "All reviews" page of a product
# Example: https://www.amazon.com/product-reviews/B07F21DSM8?sortBy=recent&m=2529788011&pageNumber=1
# Variables -> ASIN (B07F21DSM8), Page (1), Lexmark Amazon Seller ID (2529788011)
PR_URL_BASE = "https://www.amazon.com/product-reviews/"
PR_URL_PARAMS = (
    "?ie=UTF8&reviewerType=all_reviews&sortBy=recent&m=2529788011&pageNumber="
)


# URL for a particular review
# Example: https://www.amazon.com/gp/customer-reviews/R1LVMAR6YBYF7X?ASIN=B07T4LGDGQ
# Variables -> Review ID (R1LVMAR6YBYF7X), ASIN (B07T4LGDGQ)
CR_URL_BASE = "https://www.amazon.com/gp/customer-reviews/"
CR_URL_PARAMS = "?ie=UTF8&ASIN="

# Constant values
OUTPUT_NAME_PREFIX = "Scrapy_AmazonReviews_"
OUTPUT_NAME_POSTFIX = ".csv"

# Amazon Default Values, used for checking each review's data points
AMZN_DEF_UPVOTE_ONE = "One"
AMZN_DEF_OFFICIAL_COMMENT = "The manufacturer commented on the review below"
BADGE_NOT_VER = "Unverified"
BADGE_VER = "Verified Purchase"
BADGE_VINE = "Vine Customer"
LXK_AMZN_ACCNT = "Lexmark Support"

# AJAX Constants for opening comments
AMZ_AJAX_COMMENTS_URL = (
    "https://www.amazon.com/hz/reviews-render/ajax/comment/get/ref=cm_cr_arp_d_cmt_opn"
)
AMZ_AJAX_COMMENTS_HEADERS = {
    "accept": "text/html,*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,fil;q=0.8",
}
AMZ_AJAX_COMMENTS_PAYLOAD = {
    "sortCommentsBy": "newest",
    "offset": 0,
    "count": 35,
    "asin": "",
    "reviewId": "",
}

# Proper order of columns for exporting all fields
EXPRTFLDS_ALL = [
    "id",
    "date",
    "username",
    "stars",
    "model",
    "program",
    "codename",
    "purchaseType",
    "title",
    "body",
    "url",
    "upvotes",
    "comments",
    "LXKresponded",
    "reply",
    "preprocessed_body",
]

# Proper order of columns for exporting selected fields for CX
EXPRTFLDS_SELECTED = [
    "id",
    "date",
    "username",
    "stars",
    "model",
    "purchaseType",
    "title",
    "body",
    "url",
    "upvotes",
    "comments",
    "LXKresponded",
    "reply",
]






# Product Map Matrix
# Map which models belong to which codenames, and which codename belongs to program.
# [
#   [Program, Codename, [Models]],
#   [Program, Codename, [Models]],
#   [Program, Codename, [Models]]
# ]
PRODUCT_MAP = [
    ["Baja/Donzi (BD)", "Baja", ["B3442dw", "B3340dw"]],
    ["Baja/Donzi (BD)", "Donzi", ["MB3442adw"]],
    ["Big Blue/Needlefish (BBN)", "Big Blue", ["C3426dw"]],
    ["Big Blue/Needlefish (BBN)", "Needlefish", ["MC3426adw"]],
    ["Bluering/Lionfish (BRLF)", "Bluering", ["C3224dw", "C3326dw"]],
    ["Bluering/Lionfish (BRLF)", "Lionfish", ["MC3224adwe", "MC3224dwe", "MC3326adwe"]],
    ["Sidu/Goldengate (SGG)", "Sidu", ["B2236dw"]],
    ["Sidu/Goldengate (SGG)", "Goldengate", ["MB2236adwe", "MB2236adw"]],
    ["Zues/Jupiter (ZJ)", "Zues", ["C2325dw"]],
    ["Zues/Jupiter (ZJ)", "Jupiter", ["MC2425adw"]],
    ["Skyfall/Moonraker (SM)", "Skyfall", ["MB2338adw", "MB2442adwe"]]
]

# Returns the printer program and codename, given the model name.
# Program | Codename | Model
# [program, [codename1,codename2], model]
def get_program_codename(string):
    for product in PRODUCT_MAP:
        for model in product[2]:
            if model == string:
                # Input model matched with model
                # Return Program Name, Codename
                return [product[0], product[1]]
    return ["TBD", "TBD"]



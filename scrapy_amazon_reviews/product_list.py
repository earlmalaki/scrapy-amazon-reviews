########################################
# Authors:
# Earl Malaki
# Joy Trocio
########################################
# - static file that contains the following:
# -- list of products (ASIN and model)
# -- list of tracked products
########################################

# CX Watchlist
# List of printer models that CX is currently monitoring
tracked = [
    "C3224dw",
    "C3326dw",
    "MC3224adwe",
    "MC3326adwe",
    "MC3224dwe",
    "MB2236adwe",
    "MB2236adw",
    "B2236dw",
    "MC3426adw",
    "C3426dw",
    "MB3442adw",
    "B3442dw",
    "B3340dw",
]

# Master list of Lexmark products in Amazon
# Printer Model and ASIN
products = [
    {"asin": "B07T6PGM4J", "model": "C3224dw"},
    {"asin": "B07T3H979V", "model": "C3326dw"},
    {"asin": "B07T4LGDGQ", "model": "MC3224adwe"},
    {"asin": "B07T5PRRXD", "model": "MC3326adwe"},
    {"asin": "B07T1DQNNS", "model": "MC3224dwe"},
    {"asin": "B07T3HB1VZ", "model": "MB2236adwe"},
    {"asin": "B07N27LPPG", "model": "MB2236adw"},
    {"asin": "B07N23D92N", "model": "B2236dw"},
    {"asin": "B08411CN2Y", "model": "MC3426adw"},
    {"asin": "B084117J9Z", "model": "C3426dw"},
    {"asin": "B082VXTDQR", "model": "MB3442adw"},
    {"asin": "B082VY58HF", "model": "B3442dw"},
    {"asin": "B082VY2RMY", "model": "B3340dw"},
    {"model": "B2338dw", "asin": "B07F4J2STN"},
    {"model": "B2442DW", "asin": "B07F432573"},
    {"model": "C2325dw", "asin": "B07FDJQR32"},
    {"model": "MC2425adw", "asin": "B07FDJQ4JR"},
    {"model": "MB2442adwe", "asin": "B07F22K2LS"},
    {"model": "MB2338adw", "asin": "B07F21DSM8"},
]


def get_products():
    return products


def get_tracked_products():
    return tracked

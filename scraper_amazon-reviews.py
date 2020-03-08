########################################
# Author : Earl Timothy D. Malaki
# User Experience Designer
# Plaza 2 6th Floor C'10 6
# Lexmark Research and Development Cebu
########################################

########################################
# Introduction
# This script scrapes Amazon.com to gather product reviews
# This is intended to run periodically on a server, and store all data in a .csv file
# This is intended to gather reviews for all product listings of the official Lexmark Amazon Seller Page
# Last Update: February 03, 2020
########################################


# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import sys
import csv
import logging
from datetime import datetime
import html

import scraper_constants as constants
import scraper_products as products_source


########################################
# Helper Methods
########################################

# Returns the HTML block that contains the reviews
def get_reviews_body(soup):
    reviews = soup.find_all("div", {"data-hook":"review"})
    return reviews

# Returns the review details, which are the following:
# id, date, username, rating, badge, title, body
# This is done by using the css classes and/or data-hooks to locate each specific html element
def get_review_details(review, model, asin):
    id = review.get('id')

    date = review.find("span", {"data-hook":"review-date"}).get_text().strip('\n ').split(" on ")[1]


    username = review.find("span", class_="a-profile-name").get_text().strip('\n ')
    rating = review.find("span", class_="a-icon-alt").get_text().strip('\n ')[0]

    # A product listing may or may not have different versions
    # Formatstrip will not exist if the listing only has one version of the product
    try:
        variation = review.find("a", {"data-hook":"format-strip-linkless"}).get_text().strip('\n ').split(" ")[-1]
    except Exception as e:
        variation = ""

    # A review may be labelled as one of the many review types, namely
    # 'Not Verified', 'Verified Purchase', 'Vine Customer Review of Free Product', etc.
    # This section handles all cases.
    try:
        # Verified Badge
        badge = review.find("span", {"data-hook":"avp-badge"}).get_text().strip('\n ')
        badge = constants.BADGE_VER
    except Exception as e:
        eVeri = e
    try:
        # Vine Badge
        badge = review.find("span", class_="a-color-success a-text-bold").get_text().strip('\n ')
        badge = constants.BADGE_VINE
    except Exception as e:
        eBadge = e
    try:
        # Not Verified
        if (type(eVeri) is type(eBadge) and eVeri.args == eBadge.args):
            badge = constants.BADGE_NOT_VER
    except:
        pass

    # This section gets the number of upvotes a review has
    # One person found this helpful
    # x people found this helpful
    try:
        # Has upvote
        text = review.find("span", {"data-hook":"helpful-vote-statement"}).get_text().strip('\n ').split(' ')[0]
        if (text == constants.AMZN_DEF_UPVOTE_ONE):
            upvote = 1
        else:
            upvote = int(text)
    except Exception as e:
        upvote = 0

    title = review.find("a", {"data-hook":"review-title"}).get_text().strip('\n ')
    
    body = review.find("span", {"data-hook":"review-body"})
    # At this point, new lines are indicated by one <br>
    # This section replaces <br>s with a newline character "\n"
    # Then converts the entire section to text
    for br in body.find_all("br"):
        br.replace_with("\n")
    body = body.get_text().strip("\n ")

    # This section gets the number of comments in a review
    comments_count = int(review.find("span", {"class":"review-comment-total aok-hidden"}).get_text().strip('\n '))

    if (comments_count == 0):
        lxk_rep = {
            'replied': 'No',
            'reply': ""
        }
    else:
        lxk_rep = get_lxk_reply(review, asin, id)

    return {
        constants.ID: id,
        constants.DATE: date,
        constants.USERNAME: username, 
        constants.RATING: rating,
        constants.MODEL: model,
        constants.VARIATION: variation,
        constants.BADGE: badge,
        constants.UPVOTE: upvote,
        constants.COMMENTS: comments_count,
        constants.TITLE: title,
        constants.BODY: body,
        constants.LXK_REPLIED: lxk_rep['replied'],
        constants.LXK_REPLY: lxk_rep['reply']
    }

# TO DO
# Get text of reply
# Fix doesn't say Yes when lexmark comment is at next pages

# Identifies if a review has been responded to by Official Lexmark Support Amazon Account
def get_lxk_reply(review, asin, id):
    request_num = 1
    with requests.Session() as s:
        # Post AJAX request to get HTML for comments
        # Strip spaces and newlines
        # Convert to list on "&&&"
        payload = constants.AMZ_AJAX_COMMENTS_PAYLOAD
        payload['asin'] = asin
        payload['reviewId'] = id

        response = s.post(constants.AMZ_AJAX_COMMENTS_URL, payload).text.strip(' \n ').split("&&&")
        
        # Get list of comments
        # Iterate through it
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
                # End of list
                break
            
            soup = BeautifulSoup(clean, "lxml")
            
            try:
                author = soup.find("a", {"data-hook":"review-author"}).get_text().strip(' \n ')

                if (author == constants.LXK_AMZN_ACCNT):
                    # Get reply text
                    reply_text = soup.find("span", {"class":"review-comment-text"})
                    # At this point, new lines are indicated by one <br>
                    # This section replaces <br>s with a newline character "\n"
                    # Then converts the entire section to text
                    for br in reply_text.find_all("br"):
                        br.replace_with("\n")
                    reply_text = reply_text.get_text().strip("\n ")

                    return {
                        'replied': 'Yes',
                        'reply': reply_text
                        }
            except Exception as e:
                pass
        return {
            'replied': 'No',
            'reply': ""
            }
        


# Writes the list of data dictionary to a .csv file
def writeToCSV(filename, datalist):
    # Get column headers
    keys = datalist[0].keys()
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(datalist)


# Returns the URL for each specific customer review
def get_customer_review_URL(rev_ID, ASIN):
    url = constants.CR_URL_BASE + rev_ID + constants.CR_URL_PARAMS + ASIN
    return url


########################################
# Main Method
########################################
if __name__ == '__main__':
    # Setup Logger
    logging.basicConfig(filename='scraper-log.log', filemode='a', format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info('Logger initialized.')

    products = products_source.get_products()

    page_num = 1

    # List to contain the gathered data
    reviews_list = []

    for product in products:
        # Reset page counter
        page_num = 1
        with requests.Session() as s:
            # This header is critical to avoid Amazon.com flagging our scraping activity
            s.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

            logging.info("Initiating scrape sequence for " +product['model'] +" with ASIN=" +product['asin'])
            # Iterate scrape for each page of reviews for this product
            while (True):
                final_url = constants.PR_URL_BASE + product['asin'] + constants.PR_URL_PARAMS + constants.PR_URL_PAGE + str(page_num) + constants.PR_URL_SELLERID + constants.PR_SELLERID_LXK
                logging.info("Page " +str(page_num))

                response = s.get(final_url).text
                soup = BeautifulSoup(response, "lxml")

                # Get block of text pertaining to the reviews
                reviews_body = get_reviews_body(soup)
                if (len(reviews_body) == 0):
                    logging.info("Pages exhausted.")
                    break

                # Get details of each review
                for review in reviews_body:
                    details = get_review_details(review, product['model'], product['asin'])
                    details[constants.URL] = get_customer_review_URL(details[constants.ID], product['asin'])
                    reviews_list.append(details)

                # Go to next page for this product
                page_num += 1

    # Write scraped data onto a .csv file
    output_name = "scraper-outputs/"+constants.OUTPUT_NAME_PREFIX + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +constants.OUTPUT_NAME_POSTFIX
    writeToCSV(output_name, reviews_list)

########################################
# End of Main Method
########################################
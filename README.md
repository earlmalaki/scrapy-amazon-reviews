# Scrapy Amazon Reviews

A scraper made to extract product reviews for Lexmark printer products in Amazon.com. Outputs .csv files containing the following columns:
- Review ID
- Date posted
- Username
- Star rating
- Printer model
- Purchase type (Verified, Vine, etc.)
- Title
- Body
- Review url
- Number of upvotes
- Number of comments
- Replied to by Lexmark?
- Reply body
 
The scrapy was initially implemented using Requests and BeautifulSoup4. Later on rewritten on [Scrapy](https://scrapy.org) framework. 

## Requirements and Installation

Use pip to install the following dependencies:
- Beautiful Soup 4
- Requests
- Scrapy
- Scrapy UserAgents
```bash
pip install requirements.txt
```

## Usage

Change directory to the root of the project folder then run:
```bash
scrapy crawl amazon_reviews
```

## Output

The script outputs three .csv files per run. All three are stored in "amazon_reviews" folder.
- All Products - File contains all reviews for all Lexmark products in Amazon
- Tracked Products CX - File contains all reviews for the selected products that the Customer Experience team is tracking.
- PBI Report - File contains all reviews for all Lexmark products in Amazon, and contains additional information product family, preprocessed body, etc.

## Roadmap
Possible improvements are as listed:
- Scheduling the script run. Daemonizing the script and hosting it in a server, etc.
- Outputting the data to an SQL database instead of .csv file
- Categorize parts of the reviews into topics


## Authors and acknowledgment
Written by Earl Malaki
This project started as a side project/exploration for my team's benefit.
We then collaborated with various teams from other departments to make the most use out of the reviews dataset.
There's an ongoing collaboraiton with Joy Trocio to take the project further.


## License
[MIT](https://choosealicense.com/licenses/mit/)
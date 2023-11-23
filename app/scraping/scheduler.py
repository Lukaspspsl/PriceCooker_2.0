from scraper import Scraper
from db_ops import store_in_db


def periodical_scraper():
    urls = fetch_urls()  # Function to retrieve URLs from the database
    for url in urls:
        scraper = Scraper(url)
        price = scraper.extract_price()
        name = scraper.extract_name()
        store_in_db(name, price, url)

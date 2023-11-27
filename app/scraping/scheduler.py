from datetime import datetime
from threading import Thread
import time
import logging

from app import db
from app.scraping.scraper import Scraper
from app.scraping.db_ops import  store_new_price
from app.models.models import ItemModel, PriceHistoryModel
from app.db import mongo_client

@mongo_client
def fetch_urls(db=None):
    """
    Fetches URLs of all items from the database.
    """
    try:
        collection = db.items
        items = collection.find({})
        urls = [item['url'] for item in items if 'url' in item]
        return urls
    except Exception as e:
        print(f"Error fetching URLs: {e}")
        return []


def periodical_scraper(app):
    with app.app_context():
        try:
            logging.info(f"Starting periodical_scraper at {datetime.now()}")

            urls = fetch_urls()  #fetch_urls from db

            for url in urls:
                scraper = Scraper(url)
                price = scraper.extract_price()

                logging.info(f"Scraping item...")
                store_new_price(url, price)

            logging.info(f"Completed periodical_scraper at {datetime.now()}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")




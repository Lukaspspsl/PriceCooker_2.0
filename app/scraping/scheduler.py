from scraper import Scraper
from db_ops import store_in_db
from app.models.models import ItemModel

def fetch_urls():
    """
    Fetches URLs from the database.
    This function should return a list of URLs to be scraped.
    """
    items = ItemModel.find_all()
    return [item.url for item in items] if items else []


def periodical_scraper():
    urls = fetch_urls()
    for url in urls:
        scraper = Scraper(url)
        price = scraper.extract_price()
        name = scraper.extract_name()

        if price is not None and name is not None:
            store_in_db(name, price, url)

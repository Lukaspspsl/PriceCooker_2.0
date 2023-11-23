import requests
from bs4 import BeautifulSoup
import re


class Scraper:
    def __init__(self, url):
        self.url = url
        self.html_content = self.fetch_html()

    def fetch_html(self):
        response = requests.get(self.url)
        return response.text if response.status_code == 200 else None

    def extract_price(self):
        if self.html_content:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            price_tag = soup.find('span', {'class': 'price-box__price'})
            if price_tag:
                return float(re.sub(r'[^\d.]', '', price_tag.text).strip())
        return None

    def extract_name(self):
        if self.html_content:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            name_tag = soup.find('h1', {'itemprop': 'name'})
            if name_tag:
                return name_tag.text.strip()
        return None

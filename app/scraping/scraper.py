from bs4 import BeautifulSoup
import re
from security import safe_requests

#TODO: add rate limiter and headers to avoid being blocked
class Scraper:
    def __init__(self, url):
        self.url = url
        self.html_content = self.fetch_html()

    def fetch_html(self):
        """Fetch html content from url"""
        response = safe_requests.get(self.url, timeout=60)
        return response.text if response.status_code == 200 else None

    def extract_price(self):
        """Extract price from html content"""
        if self.html_content:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            price_tag = soup.find('span', {'class': 'price-box__price'})
            if price_tag:
                return float(re.sub(r'[^\d.]', '', price_tag.text).strip())
        return None

    def extract_name(self):
        """Extract name from html content"""
        if self.html_content:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            name_tag = soup.find('h1', {'itemprop': 'name'})
            if name_tag:
                return name_tag.text.strip()
        return None

from bs4 import BeautifulSoup
from utils.utils import Utils
import json


class BandcampScrapeService:
    @staticmethod
    def scrape_weekly_show(show_id: str):
        url = f"https://bandcamp.com/?show={show_id}"
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    @staticmethod
    def scrape_genre_essentials(genre: str):
        url = f"https://bandcamp.com/tag/{genre}"
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    def scrape_page(self):
        pass

from bs4 import BeautifulSoup
from utils.utils import Utils
import json


class BandcampScrapeService:
    
    @staticmethod
    def scrape_page(param: str, url: str):
        html_text = Utils.execute_get_request(url + str(param)).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

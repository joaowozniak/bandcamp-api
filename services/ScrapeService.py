from bs4 import BeautifulSoup
from utils.utils import Utils
import json


class ScrapeService:

    @staticmethod
    def scrape_page(url: str):
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    @staticmethod
    def scrape_aotd_page(url: str):
        page_html = Utils.execute_get_request(url).text
        soup = BeautifulSoup(page_html, "lxml")
        results = []
        if soup:
            for div in soup.find_all("div", {"class": "list-article aotd"}):
                for a, b in zip(div.find_all("div", {"class": "article-info-text"}),
                                div.find_all("div", {"class": "title-wrapper"})):
                    results.append(
                        [a.contents[4].strip(), b.contents[0].contents[0].strip().replace('”', '').replace('“', '')])
        return results

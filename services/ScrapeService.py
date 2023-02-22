from bs4 import BeautifulSoup
import json
from typing import List

from utils.utils import Utils


class ScrapeService:
    @staticmethod
    def scrape_page(url: str) -> dict:
        """
        Scrape the Bandcamp page at the given URL and return the data-blob as a dictionary.
        """
        html = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html, "lxml")
        if soup:
            pagedata = soup.find(id="pagedata")
            if pagedata:
                return json.loads(pagedata["data-blob"])
        return {}

    @staticmethod
    def scrape_aotd_page(url: str) -> List[List[str]]:
        """
        Scrape the Bandcamp AOTD page at the given URL and return a list of lists containing the artist name and album title.
        """
        html = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html, "lxml")
        results = []
        if soup:
            for div in soup.find_all("div", {"class": "list-article aotd"}):
                article_info = div.find("div", {"class": "article-info-text"})
                title_wrapper = div.find("div", {"class": "title-wrapper"})
                if article_info and title_wrapper:
                    artist = article_info.contents[4].strip()
                    album = title_wrapper.contents[0].contents[0].strip().replace('”', '').replace('“', '')
                    results.append([artist, album])
        return results

from services.scrape_service import ScrapeService
from services.data_load_service import DataLoadService
from fastapi import HTTPException
from utils.constants import Constants
from datetime import datetime


class AlbumOfDayService:

    # fails for date 12-01-2023
    def get_album_of_day(self, day: str):
        # Check if day parameter is valid
        if day is None:
            raise HTTPException(status_code=404, detail="Not date header found")
        self.__check_day_format(day)
        return self.__search_album_of_day(day)

    @staticmethod
    def __check_day_format(day: str):
        # Check if day parameter has valid format
        try:
            datetime.strptime(day, '%d-%m-%Y')
        except ValueError:
            raise HTTPException(status_code=404, detail="Incorrect data format, should be DD-MM-YYYY")

    def __search_album_of_day(self, day: str):
        # Search for album of the day on pages until the album is found
        albums_list = self.__estimate_page_search(day, "1")
        album_of_day = self.__filter_album_by_day(albums_list, day)
        return DataLoadService.load_album_of_day(album_of_day)

    def __estimate_page_search(self, day: str, page: str) -> str:
        # Estimate which page to search for the album of the day
        scrape_result = ScrapeService.scrape_aotd_page(Constants.album_of_day_endpoint(str(page)))
        last_day_of_page = self.__get_last_day_of_page(scrape_result)

        while datetime.strptime(last_day_of_page, Constants.DATE_FORMAT) > datetime.strptime(day, Constants.DATE_FORMAT):
            page = int(page) + 1
            scrape_result = ScrapeService.scrape_aotd_page(Constants.album_of_day_endpoint(str(page)))
            last_day_of_page = self.__get_last_day_of_page(scrape_result)

        return scrape_result

    def __get_last_day_of_page(self, aots: list) -> str:
        # Get the last day of the album of the day entries on a page
        return self.__date_formatter(aots[-1][0])

    def __filter_album_by_day(self, albums: list, day: str):
        # Filter the album of the day by the given day
        for aotd in albums:
            if day == self.__date_formatter(aotd[0]):
                return aotd
        raise HTTPException(status_code=404, detail=f"Album of day: {day} not found")

    @staticmethod
    def __date_formatter(day: str) -> str:
        # Format the day string to match the date format used in the project
        day_parsed = datetime.strptime(day, '%B %d, %Y')
        return str(day_parsed.strftime('%d-%m-%Y'))

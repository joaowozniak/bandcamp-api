from services.ScrapeService import ScrapeService
from services.DataLoadService import DataLoadService
from fastapi import HTTPException
from utils.contants import Constants
from datetime import datetime


class BandcampService:

    def get_weekly_shows(self, shows: str) -> dict:
        shows_list = {}
        valid_shows = self.__get_valid_shows(shows, self.__get_available_shows())

        if len(valid_shows) != 0:
            for sh in valid_shows:
                show_obj = self.__get_weekly_show(sh)
                shows_list[sh] = show_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Weekly Show ID not found")
        return shows_list

    def __get_weekly_show(self, show_id: str):
        if show_id not in self.__get_available_shows():
            raise HTTPException(status_code=404, detail="Bandcamp Weekly Show ID not found")
        return DataLoadService.load_tracks(show_id,
                                           ScrapeService.scrape_page(Constants.weekly_show_endpoint(show_id)))

    @staticmethod
    def __get_valid_shows(shows: str, available_shows: list) -> list:
        valid_shows = []
        for sh in shows.split(','):
            if int(sh) in available_shows:
                valid_shows.append(int(sh))

        return valid_shows

    def get_genre_essentials_list(self, genres: str) -> dict:
        genre_essentials = {}
        valid_genres = self.__get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genre in valid_genres:
                genre_ess_obj = self.__get_genre_essentials(genre, Constants.ESSENTIALS_TAB)
                genre_essentials[genre] = genre_ess_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_essentials

    @staticmethod
    def __get_genre_essentials(genre: str, tab: str) -> list:
        if genre not in Constants.ESSENTIAL_GENRES:
            raise HTTPException(status_code=404, detail=f"Bandcamp Genre Essentials not found. Genre essentials "
                                                        f"available: {Constants.ESSENTIAL_GENRES}")
        return DataLoadService.load_albums(ScrapeService.scrape_page(Constants.genre_endpoint(genre)), tab)

    @staticmethod
    def __get_valid_genres(genres: str) -> list:
        valid_genres = []
        for genre in genres.split(','):
            if genre in Constants.ESSENTIAL_GENRES:
                valid_genres.append(genre)
        return valid_genres

    def get_genre_highlights_list(self, genres: str) -> dict:
        genre_highlights = {}
        valid_genres = self.__get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genre in valid_genres:
                genre_ess_obj = self.__get_genre_essentials(genre, Constants.HIGHLIGHTS_TAB)
                genre_highlights[genre] = genre_ess_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_highlights

    @staticmethod
    def __get_available_shows() -> list:
        show_json = ScrapeService.scrape_page(Constants.weekly_show_endpoint("1"))
        return show_json["bcw_seq_details"]["show_ids"]

    def get_album_of_day(self, day: str):
        if day is None:
            raise HTTPException(status_code=404, detail="Not date header found")
        self.__check_day_format(day)
        return self.__search_album_of_day(day)

    @staticmethod
    def __check_day_format(day: str):
        try:
            datetime.strptime(day, '%d-%m-%Y')
        except ValueError:
            raise HTTPException(status_code=404, detail="Incorrect data format, should be DD-MM-YYYY")

    def __search_album_of_day(self, day: str):
        page = self.__estimate_page_search(day, "1")
        albums_list = ScrapeService.scrape_aotd_page(Constants.album_of_day_endpoint(page))
        album_of_day = self.__filter_album_by_day(albums_list, day)
        return DataLoadService.load_album_of_day(album_of_day)

    # TODO: refactor
    def __estimate_page_search(self, day: str, page) -> str:
        last_day_of_page = self.__get_last_day_of_page(
            ScrapeService.scrape_aotd_page(Constants.album_of_day_endpoint(page)))

        while datetime.strptime(last_day_of_page, Constants.DATE_FORMAT) > datetime.strptime(day,
                                                                                             Constants.DATE_FORMAT):
            page = int(page) + 1
            last_day_of_page = self.__get_last_day_of_page(
                ScrapeService.scrape_aotd_page(Constants.album_of_day_endpoint(str(page))))

        return str(page)

    def __get_last_day_of_page(self, aots):
        return self.__date_formatter(aots[-1][0])

    def __filter_album_by_day(self, albums, day):
        for aotd in albums:
            if day == self.__date_formatter(aotd[0]):
                return aotd
        raise HTTPException(status_code=404, detail=f"Album of day: {day} not found")

    @staticmethod
    def __date_formatter(day: str) -> str:
        day_parsed = datetime.strptime(day, '%B %d, %Y')
        return str(day_parsed.strftime('%d-%m-%Y'))

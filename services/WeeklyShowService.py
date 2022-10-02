from services.ScrapeService import ScrapeService
from services.DataLoadService import DataLoadService
from fastapi import HTTPException
from utils.contants import Constants


class WeeklyShowService:

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

    @staticmethod
    def __get_available_shows() -> list:
        show_json = ScrapeService.scrape_page(Constants.weekly_show_endpoint("1"))
        return show_json["bcw_seq_details"]["show_ids"]

from fastapi import HTTPException
from services.scrape_service import ScrapeService
from services.data_load_service import DataLoadService
from utils.constants import Constants


class WeeklyShowService:
    @staticmethod
    def get_weekly_shows(shows: str) -> dict:
        available_shows = WeeklyShowService.__get_available_shows()
        valid_shows = WeeklyShowService.__get_valid_shows(shows, available_shows)

        if len(valid_shows) == 0:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Weekly Show ID not found")

        shows_list = {}
        for show_id in valid_shows:
            show_obj = WeeklyShowService.__get_weekly_show(show_id, available_shows)
            shows_list[show_id] = show_obj

        return shows_list

    @staticmethod
    def __get_weekly_show(show_id: int, available_shows: list):
        if show_id not in available_shows:
            raise HTTPException(status_code=404, detail="Bandcamp Weekly Show ID not found")
        return DataLoadService.load_tracks(show_id,
                                           ScrapeService.scrape_page(Constants.weekly_show_endpoint(str(show_id))))

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

from services.ScrapeService import ScrapeService
from services.DataLoadService import DataLoadService
from fastapi import HTTPException
from utils.contants import Constants


class GenreService:

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
            if genre in Constants.ESSENTIAL_GENRES and genre not in valid_genres:
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

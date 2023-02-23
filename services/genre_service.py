from services.scrape_service import ScrapeService
from services.data_load_service import DataLoadService
from fastapi import HTTPException
from utils.constants import Constants


class GenreService:
    """
    A service for fetching genre essentials and highlights from Bandcamp.
    """

    def get_genre_essentials_list(self, genres: str) -> dict:
        """
        Returns a dictionary of essential albums for the given genres.

        :param genres: a comma-separated string of genres
        :return: a dictionary of genre names and their essential albums
        """
        genre_essentials = {}
        valid_genres = self.__get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genre in valid_genres:
                genre_essentials[genre] = self.__get_genre_essentials(genre, Constants.ESSENTIALS_TAB)
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_essentials

    def get_genre_highlights_list(self, genres: str) -> dict:
        """
        Returns a dictionary of highlight albums for the given genres.

        :param genres: a comma-separated string of genres
        :return: a dictionary of genre names and their highlight albums
        """
        genre_highlights = {}
        valid_genres = self.__get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genre in valid_genres:
                genre_highlights[genre] = self.__get_genre_essentials(genre, Constants.HIGHLIGHTS_TAB)
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_highlights

    @staticmethod
    def __get_genre_essentials(genre: str, tab: str) -> list:
        """
        Returns a list of essential or highlight albums for the given genre.

        :param genre: the name of the genre
        :param tab: the tab to scrape ('essentials' or 'highlights')
        :return: a list of album objects
        """
        if genre not in Constants.ESSENTIAL_GENRES:
            raise HTTPException(status_code=404, detail=f"Bandcamp Genre {genre} not found. Genre essentials "
                                                        f"available: {Constants.ESSENTIAL_GENRES}")
        return DataLoadService.load_albums(ScrapeService.scrape_page(Constants.genre_endpoint(genre)), tab)

    @staticmethod
    def __get_valid_genres(genres: str) -> list:
        """
        Returns a list of valid genres from the given comma-separated string.

        :param genres: a comma-separated string of genres
        :return: a list of valid genres
        """
        valid_genres = []
        for genre in genres.split(','):
            if genre in Constants.ESSENTIAL_GENRES and genre not in valid_genres:
                valid_genres.append(genre)
        return valid_genres

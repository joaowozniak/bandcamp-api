from services.BandcampScrapeService import BandcampScrapeService
from fastapi import HTTPException
from dtos.Track import Track
from dtos.WeeklyShow import WeeklyShow
from dtos.Album import Album
from utils.contants import Constants


class DataLoadService:

    def get_weekly_show_list(self, shows: list) -> dict:
        shows_list = {}
        valid_shows = self.get_valid_shows(shows, self.get_available_shows())

        if len(valid_shows) != 0:
            for sh in valid_shows:
                show_obj = self.get_weekly_show(sh)
                shows_list[sh] = show_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Weekly Show ID not found")
        return shows_list

    def get_weekly_show(self, show_id: str):
        if show_id not in self.get_available_shows():
            raise HTTPException(status_code=404, detail="Bandcamp Weekly Show ID not found")
        return self.load_tracks(show_id, BandcampScrapeService.scrape_page(show_id, Constants.WEEKLY_SHOW_ENDPOINT))

    @staticmethod
    def get_valid_shows(shows: list, available_shows: list) -> list:
        valid_shows = []
        for sh in shows[0].split(','):
            if int(sh) in available_shows:
                valid_shows.append(int(sh))

        return valid_shows

    def get_genre_essentials_list(self, genres: list) -> dict:
        genre_essentials = {}
        valid_genres = self.get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genr in valid_genres:
                genr_ess_obj = self.get_genre_essentials(genr, Constants.ESSENTIALS_TAB)
                genre_essentials[genr] = genr_ess_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_essentials

    def get_genre_essentials(self, genre: str, tab: str) -> list:
        if genre not in Constants.ESSENTIAL_GENRES:
            raise HTTPException(status_code=404, detail=f"Bandcamp Genre Essentials not found. Genre essentials "
                                                        f"available: {Constants.ESSENTIAL_GENRES}")
        return self.load_albums(BandcampScrapeService.scrape_page(genre, Constants.GENRE_ENDPOINT), tab)

    @staticmethod
    def get_valid_genres(genres: list) -> list:
        valid_genres = []
        for genr in genres[0].split(','):
            if genr in Constants.ESSENTIAL_GENRES:
                valid_genres.append(genr)
        return valid_genres

    def get_genre_highlights_list(self, genres: list) -> dict:
        genre_highlights = {}
        valid_genres = self.get_valid_genres(genres)
        if len(valid_genres) != 0:
            for genr in valid_genres:
                genr_ess_obj = self.get_genre_essentials(genr, Constants.HIGHLIGHTS_TAB)
                genre_highlights[genr] = genr_ess_obj
        else:
            raise HTTPException(status_code=404, detail="Valid Bandcamp Genre not found")
        return genre_highlights

    @staticmethod
    def get_available_shows() -> list:
        show_json = BandcampScrapeService.scrape_page("1", Constants.WEEKLY_SHOW_ENDPOINT)
        return show_json["bcw_seq_details"]["show_ids"]

    @staticmethod
    def load_albums(albums_json, tab: str) -> list:
        albums = []

        for collection in albums_json["hub"]["tabs"][0]["collections"]:
            if collection["name"] == tab:
                for album_json in collection["items"]:
                    albums.append(Album(album_json["tralbum_id"], album_json["blurb"],
                                        album_json["title"], album_json["artist"],
                                        album_json["band_url"], album_json["genre"],
                                        album_json["genre_id"], album_json["audio_url"]))
        return albums

    @staticmethod
    def load_tracks(show_id, tracks_json) -> WeeklyShow:
        tracks = []

        for track_json in tracks_json["bcw_data"][str(show_id)]["tracks"]:
            tracks.append(Track(track_json["track_id"], track_json["title"], track_json["track_url"],
                                track_json["artist"], track_json["location_text"], track_json["album_id"],
                                track_json["album_title"], track_json["band_id"], track_json["label"],
                                track_json["url"]))

        return WeeklyShow(tracks_json["bcw_data"][str(show_id)]["show_id"],
                          tracks_json["bcw_data"][str(show_id)]["date"],
                          tracks_json["bcw_data"][str(show_id)]["title"],
                          tracks_json["bcw_data"][str(show_id)]["subtitle"],
                          tracks_json["bcw_data"][str(show_id)]["desc"],
                          tracks_json["bcw_data"][str(show_id)]["audio_title"],
                          tracks_json["bcw_data"][str(show_id)]["audio_stream"],
                          tracks)

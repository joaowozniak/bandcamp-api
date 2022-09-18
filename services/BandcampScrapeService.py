from bs4 import BeautifulSoup
from dtos.Track import Track
from dtos.WeeklyShow import WeeklyShow
from utils.utils import Utils
import json
from dtos.Album import Album


class BandcampScrapeService:
    @staticmethod
    def scrape_weekly_show(show_id: int):
        url = f"https://bandcamp.com/?show={show_id}"
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    @staticmethod
    def scrape_genre_essentials(genre: str):
        url = f"https://bandcamp.com/tag/{genre}"
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    @staticmethod
    def load_albums(albums_json) -> list:
        albums = []

        for collection in albums_json["hub"]["tabs"][0]["collections"]:
            if collection["name"] == "essential_releases":
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

    def get_available_shows(self) -> list:
        show_json = self.scrape_weekly_show(1)
        return show_json["bcw_seq_details"]["show_ids"]

    @staticmethod
    def get_valid_shows(shows, available_shows):
        valid_shows = []
        for sh in shows[0].split(','):
            if int(sh) in available_shows:
                valid_shows.append(int(sh))

        return valid_shows

from bs4 import BeautifulSoup
from fastapi import HTTPException
from dtos.Track import Track
from dtos.WeeklyShow import WeeklyShow
from dtos.Album import Album
from utils.utils import Utils
import json


class BandcampScrapeService:
    essential_genres = ["electronic", "metal", "rock", "alternative", "hip-hop-rap",
                        "experimental", "punk", "pop", "ambient"]

    def scrape_weekly_show(self, show_id: int):
        available_shows = self.get_available_shows()
        if show_id not in available_shows:
            raise HTTPException(status_code=404, detail="Bandcamp Weekly Show ID not found")

        url = f"https://bandcamp.com/?show={show_id}"
        html_text = Utils.execute_get_request(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    def scrape_genre_essentials(self, genre: str):
        if genre not in self.essential_genres:
            raise HTTPException(status_code=404, detail=f"Bandcamp Genre Essentials not found. Genre essentials "
                                                        f"available: {self.essential_genres}")
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

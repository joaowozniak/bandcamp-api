from bs4 import BeautifulSoup
from dtos.Track import Track
from dtos.WeeklyShow import WeeklyShow
import json
import requests


class BandcampScrapeService:
    @staticmethod
    def scrape_weekly_show(show_id):
        url = f"https://bandcamp.com/?show={show_id}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "lxml")
        if soup:
            return json.loads(soup.find(id="pagedata")["data-blob"])

    @staticmethod
    def load_tracks(show_id, tracks_json) -> WeeklyShow:
        tracks = []

        for track_json in tracks_json["bcw_data"][str(show_id)]["tracks"]:
            print(track_json)
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

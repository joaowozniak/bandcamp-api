from dtos.Track import Track
from dtos.WeeklyShow import WeeklyShow
from dtos.Album import Album
from dtos.AlbumOfDay import AlbumOfDay


class DataLoadService:

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

    @staticmethod
    def load_album_of_day(album_info: list):
        artist, title = album_info[1].split(", ")
        day_str = album_info[0]
        return AlbumOfDay(title, artist, day_str)

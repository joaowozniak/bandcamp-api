from dtos.track import Track
from dtos.weekly_show import WeeklyShow
from dtos.album import Album


class DataLoadService:

    @staticmethod
    def load_albums(albums_json, tab: str) -> list:
        """
        Loads a list of albums from a JSON response.

        :param albums_json: The JSON response containing albums data.
        :param tab: The tab of the albums to be loaded (i.e. "Essentials", "Highlights", etc.).
        :return: A list of Album objects.
        """
        albums = []

        for collection in albums_json["hub"]["tabs"][0]["collections"]:
            if collection["name"] == tab:
                for album_json in collection["items"]:
                    album = DataLoadService.load_album_from_json(album_json)
                    albums.append(album)

        return albums

    @staticmethod
    def load_album_from_json(album_json) -> Album:
        """
        Creates an Album object from a JSON object.

        :param album_json: The JSON object containing album data.
        :return: An Album object.
        """
        artist, title = album_json["title"].split(", ")
        return Album(album_json["tralbum_id"], album_json["blurb"], title, artist,
                     album_json["band_url"], album_json["genre"], album_json["genre_id"],
                     album_json["audio_url"])

    @staticmethod
    def load_tracks(show_id, tracks_json) -> WeeklyShow:
        """
        Loads a WeeklyShow object from a JSON response.

        :param show_id: The ID of the show.
        :param tracks_json: The JSON response containing tracks data.
        :return: A WeeklyShow object.
        """
        tracks = []

        for track_json in tracks_json["bcw_data"][str(show_id)]["tracks"]:
            track = DataLoadService.load_track_from_json(track_json)
            tracks.append(track)

        return WeeklyShow(tracks_json["bcw_data"][str(show_id)]["show_id"],
                          tracks_json["bcw_data"][str(show_id)]["date"],
                          tracks_json["bcw_data"][str(show_id)]["title"],
                          tracks_json["bcw_data"][str(show_id)]["subtitle"],
                          tracks_json["bcw_data"][str(show_id)]["desc"],
                          tracks_json["bcw_data"][str(show_id)]["audio_title"],
                          tracks_json["bcw_data"][str(show_id)]["audio_stream"],
                          tracks)

    @staticmethod
    def load_track_from_json(track_json) -> Track:
        """
        Creates a Track object from a JSON object.

        :param track_json: The JSON object containing track data.
        :return: A Track object.
        """
        return Track(track_json["track_id"], track_json["title"], track_json["track_url"],
                     track_json["artist"], track_json["location_text"], track_json["album_id"],
                     track_json["album_title"], track_json["band_id"], track_json["label"],
                     track_json["url"])

    @staticmethod
    def load_album_of_day(album_info: list) -> Album:
        """
        Creates an Album object representing the album of the day.

        :param album_info: A list containing the date and album information.
        :return: An Album object.
        """
        artist, title = album_info[1].split(", ")
        day_str = album_info[0]
        return Album(None, f"Album of day: {day_str}", title, artist, None, None, None, None)

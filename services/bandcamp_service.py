from services.album_of_day_service import AlbumOfDayService
from services.genre_service import GenreService
from services.weekly_show_service import WeeklyShowService
from services.playlist_service import PlaylistService


class BandcampService:
    album_of_day = AlbumOfDayService()
    genre = GenreService()
    weekly_show = WeeklyShowService()
    playlist = PlaylistService()

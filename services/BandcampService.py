from services.AlbumOfDayService import AlbumOfDayService
from services.GenreService import GenreService
from services.WeeklyShowService import WeeklyShowService


class BandcampService:
    album_of_day = AlbumOfDayService()
    genre = GenreService()
    weekly_show = WeeklyShowService()

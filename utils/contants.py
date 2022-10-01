class Constants:
    ESSENTIAL_GENRES = ["electronic", "metal", "rock", "alternative", "hip-hop-rap",
                        "experimental", "punk", "pop", "ambient"]

    ESSENTIALS_TAB = "essential_releases"

    HIGHLIGHTS_TAB = "editors_picks"

    DATE_FORMAT = "%d-%m-%Y"

    @staticmethod
    def weekly_show_endpoint(show_id: str) -> str:
        return "https://bandcamp.com/?show=" + str(show_id)

    @staticmethod
    def genre_endpoint(genre: str) -> str:
        return "https://bandcamp.com/tag/" + str(genre)

    @staticmethod
    def album_of_day_endpoint(page: str) -> str:
        return "https://daily.bandcamp.com/album-of-the-day?page=" + str(page)

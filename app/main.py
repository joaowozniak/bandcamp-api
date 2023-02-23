from fastapi import FastAPI, Query, Header
from services.bandcamp_service import BandcampService
import uvicorn

app = FastAPI(title="Bandcamp API",
              description="Obtain bandcamp music data",
              version="1.0.0")
service = BandcampService()


@app.get("/", tags=["Services"])
def home():
    endpoints = {
        "Bandcamp Weekly endpoint": {
            "Description": "Returns the tracks of bandcamp weekly show id.",
            "URL": "/bcweekly/?shows=ID1,ID2,..."
        },
        "Bandcamp Genre Album Essentials endpoint": {
            "Description": "Returns the essential albums of genre.",
            "URL": "/genre/essentials/?genres=GENRE1,GENRE2,..."
        },
        "Bandcamp Genre Album Highlights endpoint": {
            "Description": "Returns the current album highlights of genre.",
            "URL": "/genre/highlights/?genres=GENRE1,GENRE2,..."
        },
        "Bandcamp Album Of The Day endpoint": {
            "Description": "Returns the album of day of passed date.",
            "URL": "/albumoftheday",
            "Headers": {"day": "DD-MM-YYYY"}
        }
    }

    return {"Welcome to Bandcamp API": {"Available endpoints": endpoints}}


@app.get("/bcweekly", tags=["Services"])
async def get_weekly_shows(shows: str = Query(default="1",
                                              title="Query shows",
                                              description="Get tracks of bandcamp weekly show",
                                              regex="^[0-9,]*$")):
    return service.weekly_show.get_weekly_shows(shows)


@app.get("/genre/essentials", tags=["Services"])
async def get_genre_essentials(genres: str = Query(default="pop",
                                                   title="Query genre essentials",
                                                   description="Get essentials albums of genre",
                                                   regex="[A-Za-z]")):
    return service.genre.get_genre_essentials_list(genres)


@app.get("/genre/highlights", tags=["Services"])
async def get_genre_highlights(genres: str = Query(default="pop",
                                                   title="Query genre highlights",
                                                   description="Get highlight albums of genre",
                                                   regex="[A-Za-z]")):
    return service.genre.get_genre_highlights_list(genres)


@app.get("/albumoftheday", tags=["Services"])
async def get_album_of_the_day(day: str = Header(default="30-09-2022",
                                                 title="Query album of day",
                                                 description="Get album of any given day")):
    return service.album_of_day.get_album_of_day(day)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

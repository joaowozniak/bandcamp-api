from fastapi import FastAPI, Query, Header
from services.BandcampService import BandcampService
import uvicorn

app = FastAPI(debug=True)
service = BandcampService()


@app.get("/")
def home():
    return {"Welcome to Bandcamp API":
        {"Available endpoints":
            {
                "/bcweekly/?shows=ID1,ID2,...": [{
                    "Description": "Returns the tracks of bandcamp weekly show id."}],
                "/genre/essentials/?genres=GENRE1,GENRE2,...": [
                    {"Description": "Returns the essential albums of genre."}],
                "/genre/highlights/?genres=GENRE1,GENRE2,...": [
                    {"Description": "Returns the current album highlights of genre."}],
                "/albumoftheday": [{"Description": "Returns the album of day of passed date."},
                                   {"Headers": {"dates": "DD-MM-YYYY, DD-MM-YYYY"}}]
            }
        }
    }


@app.get("/bcweekly")
async def get_weekly_shows(shows: str = Query(default=["shows"],
                                              title="Query shows",
                                              description="Get tracks of bandcamp weekly show",
                                              regex="^[0-9,]*$")):
    return service.weekly_show.get_weekly_shows(shows)


@app.get("/genre/essentials")
async def get_genre_essentials(genres: str = Query(default=["genres"],
                                                   title="Query genre essentials",
                                                   description="Get essentials albums of genre",
                                                   regex="[A-Za-z]")):
    return service.genre.get_genre_essentials_list(genres)


@app.get("/genre/highlights")
async def get_genre_highlights(genres: str = Query(default=["highlights"],
                                                   title="Query genre highlights",
                                                   description="Get highlight albums of genre",
                                                   regex="[A-Za-z]")):
    return service.genre.get_genre_highlights_list(genres)


@app.get("/aotd")
async def get_album_of_the_day(day: str = Header(description="Get album of any given day")):
    return service.album_of_day.get_album_of_day(day)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

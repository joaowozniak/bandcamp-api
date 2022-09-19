from typing import Union, List
from fastapi import FastAPI, Query
from services.DataLoadService import DataLoadService

app = FastAPI()
service = DataLoadService()


@app.get("/")
def home():
    return {"Welcome to Bandcamp API":
        {"Available endpoints":
            {
                "/bcweekly/?shows=ID1,ID2,...": [{"Description": "ETC"}],
                "/genre/essentials/?genres=GENRE1,GENRE2,...": [{"Description": "ETC"}],
                "/genre/highlights/?genres=GENRE1,GENRE2,...": [{"Description": "ETC"}],
                "/albumoftheday": [{"Description": "ETC"}, {"Headers": {"dates": "DD-MM-YYYY, DD-MM-YYYY"}}]
            }
        }
    }


@app.get("/bcweekly")
async def get_weekly_show_list(shows: Union[List[str], None] = Query(default=["shows"],
                                                                     title="Query shows",
                                                                     description="Get tracks of bandcamp weekly show",
                                                                     regex="^[0-9,]*$")):
    return service.get_weekly_show_list(shows)


@app.get("/genre/essentials")
async def get_genre_essentials_list(genres: Union[List[str], None] = Query(default=["genres"],
                                                                           title="Query genre essentials",
                                                                           description="Get essentials albums of genre",
                                                                           regex="[A-Za-z]")):
    return service.get_genre_essentials_list(genres)


@app.get("/genre/highlights")
async def get_genre_highlights_list(genres: Union[List[str], None] = Query(default=["highlights"],
                                                                           title="Query genre highlights",
                                                                           description="Get highlight albums of genre",
                                                                           regex="[A-Za-z]")):
    return service.get_genre_highlights_list(genres)

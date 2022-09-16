from typing import Union, List

from fastapi import FastAPI, Query
from services.BandcampScrapeService import BandcampScrapeService

app = FastAPI()
service = BandcampScrapeService()

available_shows = service.get_available_shows()


@app.get("/")
def home():
    return {"Hello": "Bandcamp API"}


@app.get("/bcweekly/{show_id}")
async def get_weekly_show(show_id: int):
    if show_id in available_shows:
        return service.load_tracks(show_id, service.scrape_weekly_show(show_id))
    return {"SHOW_ID EMPTY": show_id}


@app.get("/bcweekly/list/")
async def get_weekly_show_list(shows: Union[List[str], None] = Query(default=None)):
    shows_list = []
    for sh in shows[0].split(','):
        if int(sh) in available_shows:
            show_obj = await get_weekly_show(int(sh))
            shows_list.append(show_obj)
    return shows_list

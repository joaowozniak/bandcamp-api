from typing import Union, List

from fastapi import FastAPI, Query, HTTPException
from services.BandcampScrapeService import BandcampScrapeService

app = FastAPI()
service = BandcampScrapeService()
available_shows = service.get_available_shows()


@app.get("/")
def home():
    return {"Hello": "Bandcamp API"}


@app.get("/bcweekly/{show_id}")
async def get_weekly_show(show_id: int):
    if show_id not in available_shows:
        raise HTTPException(status_code=404, detail="Bandcamp Weekly Show ID not found")
    return service.load_tracks(show_id, service.scrape_weekly_show(show_id))


@app.get("/bcweekly/list/")
async def get_weekly_show_list(shows: Union[List[str], None] = Query(default=None)):
    shows_list = []
    valid_shows = service.get_valid_shows(shows, available_shows)

    if len(valid_shows) != 0:
        for sh in valid_shows:
            show_obj = await get_weekly_show(sh)
            shows_list.append(show_obj)
    else:
        raise HTTPException(status_code=404, detail="Valid Bandcamp Weekly Show ID not found")
    return shows_list


@app.get("/genre/essentials/{genre}")
async def get_genre_essentials(genre: str):
    return service.load_albums(service.scrape_genre_essentials(genre))

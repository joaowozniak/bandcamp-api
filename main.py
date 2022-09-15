from fastapi import FastAPI
from services.BandcampScrapeService import BandcampScrapeService

app = FastAPI()


@app.get("/")
def home():
    service = BandcampScrapeService()
    show = service.load_tracks(6, service.scrape_weekly_show(6))
    return {"a": show}

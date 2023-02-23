# Bandcamp API

This is a RESTful API that provides access to Bandcamp music data. It was created using the FastAPI framework.
Endpoints

### The following endpoints are currently available:
### /bcweekly

Returns the tracks of a given Bandcamp Weekly show ID.

URL: /bcweekly/?shows=ID1,ID2,...

Query Parameters:

    shows: A comma-separated list of show IDs to retrieve tracks for. Default: "1"

### /genre/essentials

Returns the essential albums of a given genre.

URL: /genre/essentials/?genres=GENRE1,GENRE2,...

Query Parameters:

    genres: A comma-separated list of genres to retrieve essential albums for. Default: "pop"

### /genre/highlights

Returns the current album highlights of a given genre.

URL: /genre/highlights/?genres=GENRE1,GENRE2,...

Query Parameters:

    genres: A comma-separated list of genres to retrieve highlight albums for. Default: "pop"

### /albumoftheday

Returns the album of the day for a given date.

URL: /albumoftheday

Headers:

    day: The date to retrieve the album of the day for, in the format "DD-MM-YYYY". Default: "30-09-2022"

Getting Started

To run the API locally, you'll need to install the dependencies listed in requirements.txt. You can do this using pip:

    pip install -r requirements.txt

Once the dependencies are installed, you can start the API server by running:

    uvicorn app.main:app --reload

## Examples

Here are some examples of how to use the Bandcamp API using curl.

### Get tracks of bandcamp weekly show:

    curl http://localhost:8000/bcweekly/?shows=1

Response:

    {
    "show_id": 1,
    "show_date": "2023-02-19",
    "tracks": [
        {
            "track_id": 1,
            "track_title": "Track 1",
            "artist_name": "Artist 1",
            "album_title": "Album 1",
            "album_id": 1,
            "genre": "Pop"
        },
        {
            "track_id": 2,
            "track_title": "Track 2",
            "artist_name": "Artist 2",
            "album_title": "Album 2",
            "album_id": 2,
            "genre": "Rock"
        }
    ]
}


### Get album of the day

    curl -H "day: 23-02-2023" http://localhost:8000/albumoftheday

Response:

    {
    "album_id": 1,
    "album_title": "Album 1",
    "artist_name": "Artist 1",
    "genre": "Pop",
    "album_description": "This is the album of the day for February 23, 2023."
    }
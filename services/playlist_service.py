import base64
import os
from io import BytesIO

import requests
import spotipy
from PIL import Image
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(dotenv_path="app/.env")


class PlaylistService:
    def __init__(self):
        self.scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private ugc-image-upload"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URI"),
            scope=self.scope
        ))

    def create_playlist_from_bcweekly(self) -> str:
        image_url = "https://cdn.imgbin.com/5/17/8/imgbin-s-l-benfica-b-uefa-europa-league-lisbon-1960-61-european-cup-benfica-Hmz5teA4P2k1fDGkZ7BcN6tCV.jpg"

        # fetch image content from the provided URL
        response = requests.get(image_url)
        if response.status_code == 200:
            image_content = response.content

        with BytesIO(image_content) as image_binary:
            # open image using PIL
            image = Image.open(image_binary)

            # convert image to base64-encoded string
            image_buffer = BytesIO()
            image.save(image_buffer, format="JPEG")
            image_data = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

            playlist_name = "BCWeekly Playlist"
            playlist_description = "A playlist created from the tracks of BCWeekly"
            playlist = self.sp.user_playlist_create(
                user=self.sp.me()["id"],
                name=playlist_name,
                description=playlist_description,
                public=True
            )

            self.sp.playlist_upload_cover_image(
                playlist_id=playlist["id"],
                image_b64=image_data
            )

            tracks = [
                {
                    "track_id": 2033603413,
                    "title": "Black Enchantment",
                    "track_url": "https://emanative.bandcamp.com/track/black-enchantment",
                    "artist": "emanative",
                    "location_text": "UK",
                    "album_id": None,
                    "album_title": None,
                    "band_id": 212035826,
                    "label": None,
                    "url": "https://emanative.bandcamp.com/track/black-enchantment"
                },
                {
                    "track_id": 2470175574,
                    "title": "Loving Free",
                    "track_url": "https://purrtapes.bandcamp.com/track/loving-free",
                    "artist": "Spazzkid",
                    "location_text": "Portland, Oregon",
                    "album_id": 3214327207,
                    "album_title": "Desire",
                    "band_id": 1254903475,
                    "label": None,
                    "url": "https://purrtapes.bandcamp.com/album/desire"
                }
            ]

            for track in tracks:
                query = f"{track['artist']} {track['title']}"
                results = self.sp.search(q=query, type="track")

                items = results.get("tracks").get("items")
                if items:
                    track_uri = items[0].get("uri")
                    self.sp.user_playlist_add_tracks(
                        user=self.sp.me()["id"],
                        playlist_id=playlist["id"],
                        tracks=[track_uri]
                    )

        return playlist["external_urls"]["spotify"]

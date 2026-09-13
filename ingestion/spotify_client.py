from dotenv import load_dotenv
import os
import base64
import requests


class SpotifyClient:
    def __init__(self):
        load_dotenv()    

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("CLIENT_ID or CLIENT_SECRET is missing.")
        
        self.token = self.get_token()



    def get_token(self):
        """Get a Spotify API access token using CLient Credentials."""

        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"

        headers = {
            "Authorization": "Basic "+ auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(url,
                                   headers = headers,
                                   data = data
                                   )

        response.raise_for_status()


        return response.json()["access_token"]
    

    def _get(self,endpoint, params=None):
        """Make an authenticated GET request to Spotify."""

        url = f"https://api.spotify.com/v1/{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        return response.json()
    
    def search_artist(self,artist_name):
        """Search for an artist by name"""

        data = self._get(
            "search",
            params = {
                "q": artist_name,
                "type": "artist",
                "limit" : 1
            }
        )

        artists = data["artists"]["items"]

        if not artists:
            return None
        
        artist = artists[0]
        return {
            "spotify_artist_id" : artist["id"],
            "artist_name" : artist["name"],
            "genres" : artist.get("genres", []),
            "followers": artist.get("followers", {}).get("total"),
            "popularity" : artist.get("popularity", None)
        }
    

    def get_artist_albums(self,artist_id):
        """Get albums and singles for an artist."""

        data = self._get(
            f"artists/{artist_id}/albums",
            params = {
                "include_groups": "album, single",
                "limit":10
            }
        )
        albums = data["items"]

        return [
            {
                "spotify_album_id": album["id"],
                "album_name": album["name"],
                "release_date": album["release_date"],
                "album_type": album["album_type"],
                "total_tracks": album["total_tracks"],
                "artist_id": artist_id
            }
            for album in albums
        ]
    

    def get_album_tracks(self,album_id):
        """Get tracks belinging to an albun"""

        data = self._get(
            f"albums/{album_id}/tracks",
            params = {
                "limit": 50
            }
        )

        tracks = data["items"]

        return [
            {
                "spotify_track_id": track["id"],
                "track_name": track["name"],
                "track_number": track["track_number"],
                "duration_ms": track["duration_ms"],
                "spotify_album_id": album_id
            }
            for track in tracks
        ]
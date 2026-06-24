from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()  # Load environment variables from .env file

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name): #search for an artist
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist found for", artist_name)
        return None
    return json_result[0]

def get_artist_albums(token, artist_id): #get albums for an artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    query = "?include_groups=album,single&limit=10"

    query_url = url + query
    result = get(query_url, headers=headers)
    albums = result.json()['items']

    # print("Status:", result.status_code)
    # print(data)

    return [
        {
            "album_id": album["id"],
            "album_name": album["name"],
            "release_date": album["release_date"],
            "album_type": album["album_type"],
            "total_tracks": album["total_tracks"],
            "artist_id": artist_id
            }
        for album in albums
    ]

def get_album_tracks(token, album_id): #get tracks for an album
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    query = "?limit=50"

    query_url = url + query
    result = get(query_url, headers=headers)
    tracks = result.json()['items']

    # print("Status:", result.status_code)
    # print(data)

    return [
        {
            "track_id": track["id"],
            "track_name": track["name"],
            "track_number": track["track_number"],
            "duration_ms": track["duration_ms"],
            "album_id": album_id
        }
        for track in tracks
    ]


def search_artist_and_get_tracks(artist_name):
    # token = get_token()
    artist = search_for_artist(token, artist_name)
    if not artist:
        return None
    artist_id = artist["id"]

    albums = get_artist_albums(token, artist_id)
    all_tracks = []

    for album in albums:
        album_id = album["album_id"]
        tracks = get_album_tracks(token, album_id)
        all_tracks.extend(tracks)

    return {
        "artist": artist,
        "albums": albums,
        "tracks": all_tracks
    }


token = get_token()

# artist = search_for_artist(token, "Olivia Rodrigo")
# artist_id = artist["id"]

# albums= get_artist_albums(token, artist_id)
# album_id = albums[0]["album_id"]  # Get the first album's ID

# tracks = get_album_tracks(token, album_id)
# datafin = search_artist_and_get_tracks("Olivia Rodrigo")


# print(albums)
datafin = search_artist_and_get_tracks("Olivia Rodrigo")

print(len(datafin["albums"]))
print(len(datafin["tracks"]))
print(datafin["tracks"][:5])
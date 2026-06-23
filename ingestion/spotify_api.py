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
    data = result.json()

    # print("Status:", result.status_code)
    # print(data)

    return data

def get_album_tracks(token, album_id): #get tracks for an album
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    query = "?limit=50"

    query_url = url + query
    result = get(query_url, headers=headers)
    data = result.json()

    # print("Status:", result.status_code)
    # print(data)

    return data



token = get_token()

result = search_for_artist(token, "Olivia Rodrigo")
artist_id = result["id"]
# albums = get_artist_albums(token, artist_id)
albums= get_artist_albums(token, artist_id)
album_lst = []
# print("Albums for artist:", result["name"])
for album in albums["items"]:
    album_lst.append(album["name"])

# print("Albums:", album_lst)
# print(artist_id)

print(get_album_tracks(token, album_id=album_lst[0])) # Example album ID
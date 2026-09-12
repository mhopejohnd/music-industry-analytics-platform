from spotify_client import SpotifyClient

spotify = SpotifyClient()


artist = spotify.search_artist("Olivia Rodrigo")

print("\nARTIST:")
print(artist)

if artist:
    tracks = spotify.get_album_tracks(
        albums[0]["spotify_album_id"]

        )
    
    print("\nTRACKS:")
    for track in tracks:
        print(track)
from spotify_client import SpotifyClient

spotify = SpotifyClient()


artist = spotify.search_artist("Olivia Rodrigo")

print("\nARTIST:")
print(artist)

if artist:
    albums = spotify.get_artist_albums(
        artist["spotify_artist_id"]
    )

    print("\nALBUMS:")
    for album in albums:
        print(album)

    if albums:
        tracks = spotify.get_album_tracks(
            albums[0]["spotify_album_id"]
        )
    
    print("\nTRACKS:")
    for track in tracks:
        print(track)
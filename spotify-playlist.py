import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# paylist_length = 400

f = open("prod/client.txt")
os.environ['SPOTIPY_CLIENT_ID'] = f.readline().strip()
os.environ['SPOTIPY_CLIENT_SECRET'] = f.readline().strip()
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8080/'
USER_ID = f.readline().strip()
scope = 'playlist-modify-private'

abs_path = os.path.dirname(__file__)
path = os.path.join(abs_path, 'test/grouped.json')
f = open(path, "r", encoding="utf8")
s = f.read().replace("'", "\'")
d = json.loads(s)

uris = []
for song in d:
    uris.append(song['spotify_uri'])

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

playlist = spotify.user_playlist_create(USER_ID, 'test', False, False, '')

spotify.playlist_add_items(playlist['uri'], uris[:100], 0)
spotify.playlist_add_items(playlist['uri'], uris[100:200], 100)
spotify.playlist_add_items(playlist['uri'], uris[200:300], 200)
spotify.playlist_add_items(playlist['uri'], uris[300:400], 300)
import os
import json

# endsong-group.py
#

abs_path = os.path.dirname(__file__)
songs = {}
count = 0

path = os.path.join(abs_path, 'out/filtered.json')
f = open(path, "r", encoding="utf8")
s = f.read().replace("'", "\'")
d = json.loads(s)
d.sort(key=lambda x: x['ts'])

for stream in d:
    if stream['spotify_track_uri'] in songs:
        songs[stream['spotify_track_uri']]['play_count'] += 1
    else:
        songs[stream['spotify_track_uri']] = {}
        songs[stream['spotify_track_uri']]['spotify_uri'] = stream['spotify_track_uri']
        songs[stream['spotify_track_uri']]['track_name'] = stream['master_metadata_track_name']
        songs[stream['spotify_track_uri']]['artist_name'] = stream['master_metadata_album_artist_name']
        songs[stream['spotify_track_uri']]['album_name'] = stream['master_metadata_album_album_name']
        songs[stream['spotify_track_uri']]['play_count'] = 1
    count += 1

lst = []
for song in songs:
    lst.append(songs[song])

lst.sort(reverse = True, key=lambda x: x['play_count'])
out = open("out/grouped.json", "w", encoding="utf8")
json.dump(lst, out, ensure_ascii=False)
out.close()
print("Wrote {} streams to output.".format(count))
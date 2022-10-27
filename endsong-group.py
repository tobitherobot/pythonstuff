import os
import json

# endsong-group.py
#
# This python script uses Spotify's entire streaming history in json format (endsong files)
# to group entries based on the number of the times a song is played.

input_file = "test/filtered.json"    # input file
output_file = "test/grouped.json"    # output file

abs_path = os.path.dirname(__file__)
songs = {}
ct_total = 0
ct_grouped = 0

path = os.path.join(abs_path, input_file)
f = open(path, "r", encoding="utf8")
s = f.read().replace("'", "\'")
d = json.loads(s)
d.sort(key=lambda x: x['ts'])

for stream in d:
    ct_total += 1
    if stream['spotify_track_uri'] in songs:
        songs[stream['spotify_track_uri']]['play_count'] += 1
    else:
        ct_grouped += 1
        songs[stream['spotify_track_uri']] = {}
        songs[stream['spotify_track_uri']]['spotify_uri'] = stream['spotify_track_uri']
        songs[stream['spotify_track_uri']]['track_name'] = stream['master_metadata_track_name']
        songs[stream['spotify_track_uri']]['artist_name'] = stream['master_metadata_album_artist_name']
        songs[stream['spotify_track_uri']]['album_name'] = stream['master_metadata_album_album_name']
        songs[stream['spotify_track_uri']]['play_count'] = 1

lst = []
for song in songs:
    lst.append(songs[song])
lst.sort(reverse = True, key=lambda x: x['play_count'])
out = open(output_file, "w", encoding="utf8")
json.dump(lst, out, ensure_ascii=False)
out.close()
print("Wrote {} out of {} streams to output.".format(ct_grouped, ct_total))
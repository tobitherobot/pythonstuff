import os
import json

# endsong-filter.py
#
# This python script uses Spotify's entire streaming history in json format (endsong files)
# to filter entries based on custom specifications (date, device).

file_count = 14             # amount of endsong files
date_limit = "2018-01-01"   # date limit; streams that day or later will be ignored

# platforms related to my devices
my_platforms = ["Windows 10 (10.0.10586; x64)", "Windows 10 (10.0.14393; x64)", "Windows 10 (10.0.15063; x64)", "Windows 7 (6.1.7601; x64; SP1; S)", "Windows 8 (6.2.9200; x64)", "Windows 8.1 (6.3.9600; x64)", "Android OS 4.4.2 API 19 (HTC, HTC One mini)", "Partner samsung_2014_tv_v7a8 Samsung 2012 TV", "Android [arm 0]", "iOS 7.0 (iPad3,6)", "iOS 7.1.2 (iPhone3,1)", "WebPlayer (websocket RFC6455)"]

abs_path = os.path.dirname(__file__)
rel_path = "prod\endsong_{}.json"
streams = []
count = 0

for i in range(file_count):

    path = os.path.join(abs_path, rel_path.format(i))
    f = open(path, "r", encoding="utf8")
    s = f.read().replace("'", "\'")
    d = json.loads(s)
    d.sort(key=lambda x: x['ts'])

    for stream in d:
        if stream['ts'][0:10] < date_limit:
            if stream['platform'] in my_platforms and stream['master_metadata_track_name'] != None:
                streams.append(stream)
                count += 1
        else:
            break
    print("Parsed endsong_{}.json...".format(i))

streams.sort(key=lambda x: x['ts'])
out = open("out/filtered.json", "w", encoding="utf8")
json.dump(streams, out, ensure_ascii=False)
out.close()    
print("Wrote {} streams to output.".format(count))

# 213.861 streams in total
#  73.109 streams before 2018
#  27.174 streams before 2018 on my platforms
#  25.163 streams with no nulls
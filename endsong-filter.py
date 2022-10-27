import os
import json

# endsong-filter.py
#
# This python script uses Spotify's entire streaming history in json format (endsong files)
# to filter entries based on custom specifications (date, device).

rel_path = "prod"           # directory path to endsong files
date_limit = "2018-01-01"   # streams that day or later will be ignored
output_limit = 13000        # max stream count in each output endsong file 

# platforms related to my devices
my_platforms = ["Windows 10 (10.0.10586; x64)", "Windows 10 (10.0.14393; x64)", "Windows 10 (10.0.15063; x64)", "Windows 7 (6.1.7601; x64; SP1; S)", "Windows 8 (6.2.9200; x64)", "Windows 8.1 (6.3.9600; x64)", "Android OS 4.4.2 API 19 (HTC, HTC One mini)", "Partner samsung_2014_tv_v7a8 Samsung 2012 TV", "Android [arm 0]", "iOS 7.0 (iPad3,6)", "iOS 7.1.2 (iPhone3,1)", "WebPlayer (websocket RFC6455)"]

abs_path = os.path.dirname(__file__)
lst = os.listdir(abs_path + '\\' + rel_path)
file_count = len(lst)
streams = []
total_count = 0
output_count = 0

for i in range(file_count):

    if 'endsong_{}.json'.format(i) not in lst:
        break

    path = os.path.join(abs_path, rel_path, 'endsong_{}.json'.format(i))
    f = open(path, "r", encoding="utf8")

    s = f.read().replace("'", "\'")
    d = json.loads(s)
    count = 0

    for stream in d:
        if stream['ts'][0:10] < date_limit and stream['platform'] in my_platforms and stream['master_metadata_track_name'] != None:
            streams.append(stream)
            total_count += 1
            count += 1
            if output_count < total_count // output_limit:
                streams.sort(key=lambda x: x['ts'])
                out = open("out/endsong_{}.json".format(output_count), "w", encoding="utf8")
                json.dump(streams, out, ensure_ascii=False)
                print("Wrote {} streams to endsong_{}.json.".format(len(streams), output_count))
                streams.clear()
                out.close() 
                output_count += 1
    print("Found {} in {} streams in endsong_{}.json...".format(count, len(d), i))

streams.sort(key=lambda x: x['ts'])
out = open("out/filtered.json", "w", encoding="utf8")
json.dump(streams, out, ensure_ascii=False)
print("Wrote {} streams to endsong_{}.json.".format(len(streams), output_count))
streams.clear()
out.close() 

# 213.861 streams in total
#  73.109 streams before 2018
#  27.174 streams before 2018 on my platforms
#  25.163 streams with no nulls
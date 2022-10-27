import os
import json

# endsong-filter.py
#
# This python script uses Spotify's entire streaming history in json format (endsong files)
# to filter entries based on custom specifications (date, device).

input_path = "test"                 # directory path to endsong files
output_file = "test/filtered.json"   # output file
upper_date_limit = "2023-01-01"     # streams that day or later will be ignored
lower_date_limit = "2019-01-01"     # streams earlier than that day will be ignored

# platforms related to my devices
my_platforms = ["Android [arm 0]", "Windows 10 (10.0.10586; x64)", "Windows 10 (10.0.14393; x64)", "Windows 10 (10.0.15063; x64)", "Windows 7 (6.1.7601; x64; SP1; S)", "Windows 8 (6.2.9200; x64)", "Windows 8.1 (6.3.9600; x64)", "Android OS 4.1.2 API 16 (samsung, GT-I8190N)", "Android OS 4.1.2 API 16 (samsung, GT-I9300)", "Android OS 4.3 API 18 (samsung, GT-I9300)", "Android OS 4.4.2 API 19 (HTC, HTC One mini)", "iOS 7.0 (iPad3,6)", "iOS 7.1.2 (iPhone3,1)", "iOS 8.1.1 (iPad3,6)", "iOS 9.2 (iPad3,6)", "iOS 9.3.4 (iPad3,6)", "iOS 9.3.5 (iPad3,6)", "iOS 10.0.2 (iPad3,6)", "iOS 10.2.1 (iPad3,6)", "WebPlayer (websocket RFC6455)", "Partner samsung_2014_tv_v7a8 Samsung 2012 TV"]

abs_path = os.path.dirname(__file__)
lst = os.listdir(abs_path + '\\' + input_path)
file_count = len(lst)
streams = []
output_count = 0
ct_total = 0
ct_filtered = 0

for i in range(file_count):

    if 'endsong_{}.json'.format(i) not in lst:
        break

    path = os.path.join(abs_path, input_path, 'endsong_{}.json'.format(i))
    f = open(path, "r", encoding="utf8")
    s = f.read().replace("'", "\'")
    d = json.loads(s)
    ct_tmp_total = 0
    ct_tmp_filtered = 0

    for stream in d:
        ct_total += 1
        ct_tmp_total += 1
        if lower_date_limit <= stream['ts'][0:10] and stream['ts'][0:10] < upper_date_limit and stream['platform'] not in my_platforms and stream['master_metadata_track_name'] != None and 10000 < stream['ms_played']:
            ct_filtered += 1
            ct_tmp_filtered += 1
            streams.append(stream)
    print("Found {} out of {} streams in endsong_{}.json...".format(ct_tmp_filtered, ct_tmp_total, i))

streams.sort(key=lambda x: x['ts'])

idx = []
for i in range(len(streams)-1):
    if streams[i]['ts'] == streams[i+1]['ts']:
        idx.append(i+1)
idx = idx[::-1]
for i in idx:
    streams.pop(i)
    ct_filtered -= 1

out = open(output_file, "w", encoding="utf8")
json.dump(streams, out, ensure_ascii=False)
streams.clear()
out.close()
print("Wrote {} out of {} streams to output.".format(ct_filtered, ct_total))
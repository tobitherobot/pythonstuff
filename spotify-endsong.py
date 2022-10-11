import os
import json

file_count = 14
limit_year = "2018"

abs_path = os.path.dirname(__file__)
rel_path = "prod\endsong_{}.json"
my_platforms = ["Windows 10 (10.0.10586; x64)", "Windows 10 (10.0.14393; x64)", "Windows 10 (10.0.15063; x64)", "Windows 7 (6.1.7601; x64; SP1; S)", "Windows 8 (6.2.9200; x64)", "Windows 8.1 (6.3.9600; x64)", "Android OS 4.4.2 API 19 (HTC, HTC One mini)", "Partner samsung_2014_tv_v7a8 Samsung 2012 TV", "Android [arm 0]", "iOS 7.0 (iPad3,6)", "iOS 7.1.2 (iPhone3,1)", "WebPlayer (websocket RFC6455)"]
streams = []
count = 0
ptfrms = set()

for i in range(file_count):

    path = os.path.join(abs_path, rel_path.format(i))
    f = open(path, "r", encoding="utf8")

    s = f.read().replace("'", "\'")
    d = json.loads(s)
    d.sort(key=lambda x: x['ts'])

    for stream in d:
        if stream['ts'][0:4] < limit_year:
            if stream['platform'] in my_platforms:
                streams.append(stream)
                ptfrms.add(stream['platform'])
                count += 1
        else:
            break
    print("Parsed endsong_{}.json...".format(i))

streams.sort(key=lambda x: x['ts'])
out = open("output.json", "w", encoding="utf8")
json.dump(streams, out, ensure_ascii=False)
out.close()    
print("Wrote {} streams to output.".format(count))
import os
import json

file_count = 14
limit_year = "2018"

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
        if stream['ts'][0:4] < limit_year:
            streams.append(stream)
            count += 1
        else:
            break
    print("Parsed endsong_{}.json...".format(i))

streams.sort(key=lambda x: x['ts'])
out = open("output.json", "w", encoding="utf8")
json.dump(streams, out, ensure_ascii=False)
out.close()    
print("Wrote {} streams to output...".format(count))
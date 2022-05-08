import json
import os
from datetime import datetime


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.makedirs(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

data = load_json("./打包.json")

d = []

for i in data:
    if datetime.strptime(i["ModTime"],"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None) >= datetime.strptime("2022-4-20","%Y-%m-%d"):
        continue
    d.append({
        "name":i["Name"],
        "date":i["ModTime"],
    })
print("len(data)",len(data))
print("len(d)",len(d))
save("./","打包2",json.dumps(d))

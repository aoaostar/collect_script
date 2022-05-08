# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/3/30
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import json
import os
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from tqdm import tqdm

data_path = './data'
listdir = os.listdir(data_path)
listdir.sort(key=lambda x: int(x[5:-5]))
listdir = listdir[4001:5001]

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


# if __name__ == '__main__':
#     print("正在扫描空白页（未采集成功的）")
#     path = './data'
#     listdir = os.listdir(path)
#     empty_list = []
#     for dir in listdir:
#         data = load_json(path + '/' + dir)
#         if len(data) <= 0:
#             empty_list.append(re.findall('\d+', dir)[0])
#     print(f"扫描完毕，共{len(empty_list)}页为空")
#     print(empty_list)
#
# if __name__ == '__main__':
#     print("正在扫描遗漏的")
#     path = './data'
#     listdir = os.listdir(path)
#     empty_list = []
#     for i in range(0,7004):
#         if not f"page_{i}.json" in listdir:
#             empty_list.append(i)
#
#     print(f"扫描完毕，共{len(empty_list)}页未采集")
#     print(json.dumps(empty_list))

def scan(data, page, bar):
    bar.set_description(page)
    failed = []
    for item in data:
        filename = item['id'].replace('/', '_')
        extensions_list = [item['extension'], ".jpg", ".jpeg", ".png", ".gif"]
        for x in extensions_list.copy():
            extensions_list.append(x.upper())
        extensions = sorted(set(extensions_list), key=extensions_list.index)
        for index in range(len(extensions)):
            filepath = f"./images/{page}/{filename}{extensions[index]}"
            if os.path.exists(filepath) and os.path.getsize(filepath) > 10240:
                break
            if index + 1 == len(extensions):
                failed.append({
                    "item": item,
                    "page": page
                })
                break
    bar.update(1)
    return failed


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.mkdir(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()


if __name__ == '__main__':
    print("计算遗漏（未采集成功的,落下的）")
    failed_list = []
    total = 0
    bar = tqdm(total=len(listdir), ascii=True)
    pool = ThreadPoolExecutor(max_workers=20)
    tasks = []
    for dir in listdir:
        page = dir[:-5]
        data = load_json(data_path + '/' + dir)
        total += len(data)
        tasks.append(pool.submit(scan, data, page, bar))
    for future in as_completed(tasks):
        failed_list.extend(future.result())

    print(f"扫描完毕，共{total}张图片，共{len(failed_list)}张无效")
    scan_list = {}
    for item in failed_list:
        if not item["page"] in scan_list:
            scan_list[item["page"]] = []
        scan_list[item["page"]].append(item["item"])
    for page in scan_list:
        save("./scan", page, json.dumps(scan_list[page]), ".json")

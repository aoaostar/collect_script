# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/3/30
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import asyncio
import json
import os

import aiohttp

if __name__ != '__main__':
    os._exit()


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def http_get(url, params=None):
    if params is None:
        params = {}
    url = PROXY + url
    return aiohttp.request("GET", url, params=params, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36",
    }, timeout=aiohttp.ClientTimeout(total=TIMEOUT))


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.makedirs(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()


def save_file(output, filename, contents, extension='.jpg'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.makedirs(output)
    with open(path, "wb") as f:
        f.write(contents)
        f.flush()


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


async def download(data):
    filename = data['item']['id'].replace('/', '_')
    extensions_list = [data['item']['extension'], ".jpg", ".jpeg", ".png", ".gif"]
    for x in extensions_list.copy():
        extensions_list.append(x.upper())
    extensions = sorted(set(extensions_list), key=extensions_list.index)
    flag = False
    for extension in extensions:
        if flag:
            break
        filepath = f"./images/{data['page']}/{filename}{extension}"
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10240:
            break
        for i in range(3):
            try:
                async with http_get(
                        f"https://images.anime-pictures.net/{data['item']['id']}{extension}") as r:
                    if r.status != 200:
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                        break
                    save_file(f"./images/{data['page']}", filename, await r.read(), extension)
                    flag = True
                    break
            except Exception as e:
                print(f"[{filename}{extension}]???????????????{e}")
                continue


async def page_down(image_dict, page):
    images_count = len(image_dict)
    print(f"??????{images_count}????????????????????????~")
    tasks = []
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    from tqdm.asyncio import tqdm
    pbar = tqdm(total=images_count, desc="ANIME-PICTURES??????", ascii=True)
    for index in range(len(image_dict)):
        tasks.append(asyncio.create_task(
            semap(semaphore, download,
                  {
                      "page": page,
                      "index": index,
                      "item": image_dict[index]
                  },
                  lambda x: pbar.update(1) and pbar.set_description(
                      f"ANIME-PICTURES?????? ???{x['page']}??? ???{x['index'] + 1}???"))))
    if len(tasks) > 0:
        await asyncio.wait(tasks)


async def main():
    print(f"????????????~ ??????{len(NEED_DOWNLOAD_PAGES)}???")
    images_count = 0
    for dir in NEED_DOWNLOAD_PAGES:
        data = load_json(DATA_PATH + "/" + dir)
        page = dir[:-len(".json")]
        print(f"???????????????{page}??? ???{len(data)}?????????")
        await page_down(data, page)
        print(f"???{page}???????????????")
        images_count += len(data)

    print(f"?????????????????? ??????{images_count}?????????")


# ?????????
MAX_WORKERS = 15
# ??????????????????
DATA_PATH = './scan'
# DATA_PATH = './data'
listdir = os.listdir(DATA_PATH)
listdir.sort(key=lambda x: int(x[5:-5]))

NEED_DOWNLOAD_PAGES = listdir
# NEED_DOWNLOAD_PAGES = listdir[1400:4001]
# NEED_DOWNLOAD_PAGES = listdir[4001:5001]
# NEED_DOWNLOAD_PAGES = listdir[5001:]


# http??????
PROXY = ''
# ????????????
TIMEOUT = 120
loop = asyncio.get_event_loop()

loop.run_until_complete(main())

# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/3/30
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------

import asyncio
import json
import os
import re

import aiohttp

from bs4 import BeautifulSoup


def http_get(url, params=None):
    if params is None:
        params = {}
    return aiohttp.request("GET", url, params=params, proxy=PROXY, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36",
    })


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.mkdir(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


async def collect_url(page):
    url = f"https://anime-pictures.net/pictures/view_posts/{page}?order_by=date_r&ldate=0&lang=zh_CN"
    image_list = []
    async with http_get(url) as r:
        res = await r.text()
        soup = BeautifulSoup(res, "html.parser")
        soup_select = soup.select("#posts .posts_block .img_cp")
        for img in soup_select:
            src = img.get('src')
            re_search = re.search('//cdn.anime-pictures.net/previews/([a-z\d]+/[a-z\d]+)_cp(.[a-z]+)', src)
            image_list.append({
                "id": re_search.group(1),
                "extension": re_search.group(2),
            })
    save('./data', f"page_{page}", json.dumps(image_list))
    return {
        "page": page,
        "list": image_list
    }


async def main():
    print("ANIME-PICTURES 开始采集~")
    tasks = []
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    from tqdm.asyncio import tqdm
    pbar = tqdm(total=len(PAGES), ascii=True)
    for page in PAGES:
        tasks.append(asyncio.create_task(semap(semaphore, collect_url, page,
                                               lambda x: pbar.update(1) and pbar.set_description(
                                                   f"ANIME-PICTURES采集 第{x}页"))))
    await asyncio.wait(tasks)
    count = 0
    for k in range(len(tasks)):
        r = tasks[k].result()
        count += len(r['list'])
    pbar.close()
    print(f"[ANIME-PICTURES]采集完毕，共{count}张图片")


# 并行数
MAX_WORKERS = 10
# http代理
PROXY = ''
PAGES = range(0, 7002 + 1)
loop = asyncio.get_event_loop()

loop.run_until_complete(main())

loop.close()

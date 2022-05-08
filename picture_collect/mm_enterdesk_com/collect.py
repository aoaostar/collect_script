# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/19
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
# https://mm.enterdesk.com/1.html

import asyncio
import json
import os

import aiohttp
from bs4 import BeautifulSoup


def http_get(url, params=None):
    if params is None:
        params = {}
    return aiohttp.request("GET", url, params=params, proxy=PROXY, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36",
        "Host": "mm.enterdesk.com",
        "Referer": "https://mm.enterdesk.com",
        "X-Requested-With": "XMLHttpRequest",
    }, timeout=aiohttp.ClientTimeout(total=TIMEOUT))


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.makedirs(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()


async def collect(data):
    result = []
    for _ in range(3):
        async with http_get(data["url"]) as r:
            if r.status != 200:
                continue
            soup = BeautifulSoup(await r.text(), "html.parser")
            select = soup.select("a.pics_pics")
            if len(select) == 0:
                continue
            for item in select:
                href = item.get('src').replace('edpic', 'edpic_source')
                result.append(href)
            print(f"[{data['id']}] 采集完毕", len(result))
            break
    return data['id'], result


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


async def main():
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    tasks = []
    failed = []
    print(f"开始采集,共{len(URL_LIST)}页")

    try:
        for id in URL_LIST:
            tasks.append(asyncio.create_task(semap(semaphore, collect, {
                "id": id,
                "url": URL_LIST[id],
            }, None)))
        await asyncio.wait(tasks)
        for task in tasks:
            page, res = task.result()
            COLLECT_URL_LIST.update({
                page: res
            })
            if len(res) == 0:
                failed.append(page)
        print("采集完毕", len(COLLECT_URL_LIST), "失败个数", len(failed))
    finally:
        save('./', 'data.collect', json.dumps(COLLECT_URL_LIST))
        if len(failed) > 0:
            save('./', 'failed.collect', json.dumps(failed))


PROXY = ''
# 超时时间
TIMEOUT = 120
MAX_WORKERS = 5
URL_LIST = load_json('./data.json')
COLLECT_URL_LIST = load_json('./data.collect.json')

URL_LIST = {val: URL_LIST[val] for val in URL_LIST if val not in COLLECT_URL_LIST.keys()}

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

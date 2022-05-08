# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/17
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------

# http://wallpaper.apc.360.cn/index.php?c=WallPaper&start=0&count=200&from=360chrome&a=getAppsByCategory&cid=6
import asyncio
import json
import math
import os

import aiohttp


def http_get(url, params=None):
    if params is None:
        params = {}
    return aiohttp.request("GET", url, params=params, proxy=PROXY, headers={
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


async def collect(params):
    result = {}
    for _ in range(3):
        async with http_get(
                f'http://wallpaper.apc.360.cn/index.php?c=WallPaper&start={params["page"]}&count={params["limit"]}&from=360chrome&a=getAppsByCategory&cid=6') as r:
            if r.status != 200:
                continue
            resp = await r.json()
            if "data" in resp:
                for item in resp["data"]:
                    result.update({
                        item["id"]: item["url"],
                    })
            print(f"第{params['page']}页采集完毕", len(result))
            break
    return result


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


async def main():
    semaphore = asyncio.Semaphore(5)
    tasks = []
    result = {}
    for i in range(1, math.ceil(TOTAL_COUNT / 12) + 1):
        tasks.append(asyncio.create_task(semap(semaphore, collect, {
            "page": i,
            "limit": 12,
        }, None)))

    await asyncio.wait(tasks)
    for task in tasks:
        result.update(task.result())
    print("采集完毕", len(result))
    save('./', 'data', json.dumps(result))


PROXY = ''
# 超时时间
TIMEOUT = 120
PAGE = 1
TOTAL_COUNT = 7401

loop = asyncio.get_event_loop()

loop.run_until_complete(main())
loop.close()

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
    url = PROXY + url
    return aiohttp.request("GET", url, params=params, headers={
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


async def collect(page):
    result = {}
    for _ in range(3):
        async with http_get(
                f'https://mm.enterdesk.com/{page}.html') as r:
            if r.status != 200:
                continue
            soup = BeautifulSoup(await r.text(), "html.parser")
            select = soup.select(".egeli_pic_li a")
            if len(select) == 0:
                continue
            for item in select:
                href = item.get('href')
                id = href[href.rindex("/") + 1:-len('.html')]
                result[id] = href
            print(f"第{page}页采集完毕", len(result))
            break
    return page, result


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


async def main():
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    tasks = []
    result = {}
    failed = []
    print(f"开始采集PAGE={PAGE},MAX_PAGE={MAX_PAGE}")

    for i in range(1, MAX_PAGE + 1):
        tasks.append(asyncio.create_task(semap(semaphore, collect, i, None)))

    try:
        await asyncio.wait(tasks)
        for task in tasks:
            page, res = task.result()
            result.update(res)
            if len(res) == 0:
                failed.append(page)
        print("采集完毕", len(result), "失败个数", len(failed))
    finally:
        save('./', 'data', json.dumps(result))
        if len(failed) > 0:
            save('./', 'failed', json.dumps(failed))


PROXY = ''
# 超时时间
TIMEOUT = 120
PAGE = 1
MAX_PAGE = 242
MAX_WORKERS = 5

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

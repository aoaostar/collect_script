# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/19
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import asyncio
import json
import os

import aiohttp
from bs4 import BeautifulSoup

URL_LIST = ["https://www.soumeitu.com/68655.html", "https://www.soumeitu.com/68649.html",
            "https://www.soumeitu.com/68646.html", "https://www.soumeitu.com/68640.html",
            "https://www.soumeitu.com/68637.html", "https://www.soumeitu.com/68634.html",
            "https://www.soumeitu.com/68628.html", "https://www.soumeitu.com/68625.html",
            "https://www.soumeitu.com/68578.html", "https://www.soumeitu.com/50565.html",
            "https://www.soumeitu.com/50535.html", "https://www.soumeitu.com/50335.html",
            "https://www.soumeitu.com/49955.html", "https://www.soumeitu.com/49947.html",
            "https://www.soumeitu.com/49514.html", "https://www.soumeitu.com/49211.html",
            "https://www.soumeitu.com/49200.html", "https://www.soumeitu.com/48153.html",
            "https://www.soumeitu.com/48078.html", "https://www.soumeitu.com/47563.html",
            "https://www.soumeitu.com/47552.html", "https://www.soumeitu.com/47362.html",
            "https://www.soumeitu.com/47314.html", "https://www.soumeitu.com/46911.html",
            "https://www.soumeitu.com/46676.html", "https://www.soumeitu.com/46290.html",
            "https://www.soumeitu.com/43267.html", "https://www.soumeitu.com/43256.html",
            "https://www.soumeitu.com/43245.html", "https://www.soumeitu.com/43234.html",
            "https://www.soumeitu.com/41283.html", "https://www.soumeitu.com/41012.html",
            "https://www.soumeitu.com/37757.html", "https://www.soumeitu.com/37743.html",
            "https://www.soumeitu.com/37651.html", "https://www.soumeitu.com/37635.html",
            "https://www.soumeitu.com/37518.html", "https://www.soumeitu.com/37491.html",
            "https://www.soumeitu.com/37327.html", "https://www.soumeitu.com/37247.html",
            "https://www.soumeitu.com/37239.html", "https://www.soumeitu.com/37212.html",
            "https://www.soumeitu.com/37158.html", "https://www.soumeitu.com/36209.html",
            "https://www.soumeitu.com/35642.html", "https://www.soumeitu.com/35618.html",
            "https://www.soumeitu.com/35545.html", "https://www.soumeitu.com/35521.html",
            "https://www.soumeitu.com/35500.html", "https://www.soumeitu.com/35476.html",
            "https://www.soumeitu.com/35468.html", "https://www.soumeitu.com/34654.html",
            "https://www.soumeitu.com/34648.html", "https://www.soumeitu.com/34621.html",
            "https://www.soumeitu.com/34613.html", "https://www.soumeitu.com/33467.html",
            "https://www.soumeitu.com/33359.html", "https://www.soumeitu.com/33316.html",
            "https://www.soumeitu.com/32049.html", "https://www.soumeitu.com/32034.html",
            "https://www.soumeitu.com/32014.html", "https://www.soumeitu.com/31658.html",
            "https://www.soumeitu.com/31648.html", "https://www.soumeitu.com/31470.html",
            "https://www.soumeitu.com/31459.html", "https://www.soumeitu.com/31445.html",
            "https://www.soumeitu.com/30347.html", "https://www.soumeitu.com/30135.html",
            "https://www.soumeitu.com/30118.html", "https://www.soumeitu.com/30066.html",
            "https://www.soumeitu.com/30046.html", "https://www.soumeitu.com/30146.html",
            "https://www.soumeitu.com/30028.html", "https://www.soumeitu.com/30017.html",
            "https://www.soumeitu.com/29996.html", "https://www.soumeitu.com/29985.html",
            "https://www.soumeitu.com/29979.html", "https://www.soumeitu.com/29535.html",
            "https://www.soumeitu.com/29472.html", "https://www.soumeitu.com/29320.html",
            "https://www.soumeitu.com/25522.html", "https://www.soumeitu.com/25502.html",
            "https://www.soumeitu.com/25447.html", "https://www.soumeitu.com/24969.html",
            "https://www.soumeitu.com/24934.html", "https://www.soumeitu.com/24876.html",
            "https://www.soumeitu.com/24020.html", "https://www.soumeitu.com/24009.html",
            "https://www.soumeitu.com/23992.html", "https://www.soumeitu.com/23981.html",
            "https://www.soumeitu.com/23961.html", "https://www.soumeitu.com/23942.html",
            "https://www.soumeitu.com/23934.html", "https://www.soumeitu.com/23924.html",
            "https://www.soumeitu.com/23914.html", "https://www.soumeitu.com/23903.html",
            "https://www.soumeitu.com/23615.html", "https://www.soumeitu.com/23398.html",
            "https://www.soumeitu.com/23391.html", "https://www.soumeitu.com/23383.html",
            "https://www.soumeitu.com/23372.html", "https://www.soumeitu.com/23362.html",
            "https://www.soumeitu.com/23352.html", "https://www.soumeitu.com/23102.html",
            "https://www.soumeitu.com/23092.html", "https://www.soumeitu.com/23083.html",
            "https://www.soumeitu.com/23069.html", "https://www.soumeitu.com/23060.html",
            "https://www.soumeitu.com/23044.html", "https://www.soumeitu.com/22978.html",
            "https://www.soumeitu.com/22948.html", "https://www.soumeitu.com/22908.html",
            "https://www.soumeitu.com/22861.html", "https://www.soumeitu.com/34640.html",
            "https://www.soumeitu.com/22631.html", "https://www.soumeitu.com/22610.html",
            "https://www.soumeitu.com/22602.html", "https://www.soumeitu.com/22543.html",
            "https://www.soumeitu.com/22529.html", "https://www.soumeitu.com/21581.html",
            "https://www.soumeitu.com/21219.html", "https://www.soumeitu.com/21196.html",
            "https://www.soumeitu.com/18973.html", "https://www.soumeitu.com/18832.html",
            "https://www.soumeitu.com/17124.html", "https://www.soumeitu.com/17107.html",
            "https://www.soumeitu.com/15801.html", "https://www.soumeitu.com/15746.html",
            "https://www.soumeitu.com/15597.html", "https://www.soumeitu.com/15587.html",
            "https://www.soumeitu.com/15564.html", "https://www.soumeitu.com/15490.html",
            "https://www.soumeitu.com/14724.html", "https://www.soumeitu.com/14250.html",
            "https://www.soumeitu.com/13275.html", "https://www.soumeitu.com/12858.html",
            "https://www.soumeitu.com/12687.html", "https://www.soumeitu.com/12594.html",
            "https://www.soumeitu.com/12562.html", "https://www.soumeitu.com/11721.html",
            "https://www.soumeitu.com/11616.html", "https://www.soumeitu.com/11602.html",
            "https://www.soumeitu.com/9573.html", "https://www.soumeitu.com/9289.html",
            "https://www.soumeitu.com/9278.html", "https://www.soumeitu.com/9212.html",
            "https://www.soumeitu.com/9036.html", "https://www.soumeitu.com/9011.html",
            "https://www.soumeitu.com/8985.html", "https://www.soumeitu.com/8871.html",
            "https://www.soumeitu.com/8850.html"]


def save(output, filename, contents, extension='.json'):
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.makedirs(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


def http_get(url, params=None):
    if params is None:
        params = {}
    url = PROXY + url
    return aiohttp.request("GET", url, params=params, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36",
    }, timeout=aiohttp.ClientTimeout(total=TIMEOUT))


async def collect(url):
    result = []
    id = url[url.rindex('/') + 1:-len('.html')]
    url = f"https://www.soumeitu.com/{id}/all.html"
    for _ in range(3):
        async with http_get(url) as r:
            if r.status != 200:
                continue
            soup = BeautifulSoup(await r.text(), "html.parser")
            select = soup.select("a.imageclick-href img")
            if len(select) == 0:
                continue
            for item in select:
                href = item.get('src')
                result.append(href)
            print(f"id={id}采集完毕", len(result))
            break
    return id, result


async def main():
    tasks = []
    result = {}
    failed = []
    semaphore = asyncio.Semaphore(5)

    print(f"开始采集,总共={len(URL_LIST)}")

    for url in URL_LIST:
        tasks.append(asyncio.create_task(semap(semaphore, collect, url, None)))

    try:
        await asyncio.wait(tasks)
        for task in tasks:
            id, res = task.result()
            result.update({
                id: res
            })
            if len(res) == 0:
                failed.append(id)
        print("采集完毕", len(result), "失败个数", len(failed))
    finally:
        save('./', 'data.collect', json.dumps(result))
        if len(failed) > 0:
            save('./', 'failed.collect', json.dumps(failed))


# PROXY = 'https://proxy.aoaostar.workers.dev/'
PROXY = ''
# 超时时间
TIMEOUT = 120
PAGE = 1
MAX_PAGE = 242
MAX_WORKERS = 5

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

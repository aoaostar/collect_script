# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/1/18
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------

import asyncio
import json
import os

import aiohttp
from bs4 import BeautifulSoup


def http_get(url, params=None):
    if params is None:
        params = {}
    return aiohttp.request("GET", url, params=params, proxy=PROXY)


async def get_novel_chapters(url):
    async with http_get(url) as r:
        res = await r.text()
        soup = BeautifulSoup(res, "html.parser")
        soup_select = soup.select(f"#list > dl > dd:nth-child(n+{REDUNDANT_CHAPTERS + 3}) > a")
        chapters = []
        from urllib import parse
        for item in soup_select:
            chapters.append({
                "url": parse.urljoin(url, item.get('href')),
                "title": item.string.strip(),
            })
        return chapters


async def collect_contents(data):
    contents = []
    for i in range(3):
        try:
            async with http_get(data["url"]) as r:
                res = await r.text(errors='ignore')
                soup = BeautifulSoup(res, "html.parser")
                find = soup.find("div", id='content')
                for p in find.contents:
                    replace = str(p).replace("<br/>", "\n")
                    replace2 = BeautifulSoup(replace, "html.parser")
                    contents.append(replace2.get_text())
            break
        except:
            continue
    return "\n".join(contents)


async def semap(sem, func, data, callback=None):
    async with sem:
        res = await func(data)
        if callback:
            callback(data)
        return res


def save(output, filename, contents, extension='.txt'):
    # 保存成txt
    output = output.rstrip('/\\')
    path = f"{output}/{filename}{extension}"
    if not os.path.exists(output):
        os.mkdir(output)

    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)
        f.flush()
    print(f"[{filename}]写出成功，[{path}]")


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


async def main():
    chapters = await get_novel_chapters(NOVEL_URL)
    print(f"开始采集，共计{len(chapters)}章")
    tasks = []
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    from tqdm.asyncio import tqdm
    pbar = tqdm(total=len(chapters), desc=NOVEL_TITLE, ascii=True)
    for chapter in chapters:
        tasks.append(asyncio.create_task(semap(semaphore, collect_contents, chapter,
                                               lambda x: pbar.update(1) and pbar.set_description(x["title"]))))
    await asyncio.wait(tasks)
    chapter_contents = NOVEL_TITLE + "\n\n"
    try:
        for k in range(len(tasks)):
            chapter_contents += "\n" + chapters[k]['title'].strip() + "\n" + tasks[k].result().strip()
    finally:
        save(OUPUT, NOVEL_TITLE, chapter_contents.strip("\n"))
    pbar.close()
    print(f"[{NOVEL_TITLE}]采集完毕，共{len(chapters)}章")


OUPUT = "./output"
NOVEL_URL = "https://www.xbiquge.so/book/52882/"
NOVEL_TITLE = "重生1991"
DATA_PATH = "./"
# 并行数
MAX_WORKERS = 10
# 第一栏多余章节数目，需要去除
REDUNDANT_CHAPTERS = 12
# http代理
PROXY = ''
# PROXY = ''

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/1/18
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------

import asyncio
import json
import os
import re
import sys

import aiohttp


def http_get(url, params=None):
    if params is None:
        params = {}
    return aiohttp.request("GET", url, params=params, proxy=PROXY)


async def get_novels_list():
    async with http_get('https://book.xbookcn.net') as r:
        res = await r.text()
        pattern = re.compile('''<a dir='ltr' href='(.+?)'>(.+?)</a>''', )
        findall = pattern.findall(res)
        novels = []
        for item in findall:
            if item[1] in ['目录索引', '联系方式']:
                continue
            novels.append({
                "url": item[0],
                "title": item[1],
            })
        return novels


async def get_novel_chapters(novel):
    async with http_get(novel['url'], params={
        "max-results": "9999999"
    }) as r:
        res = await r.text()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res, "html.parser")
        soup_select = soup.select("h3[class='post-title entry-title'] a")
        chapters = []
        for item in soup_select:
            chapters.append({
                "url": item.get('href'),
                "title": item.string,
            })
        return chapters


async def collect_contents(data):
    contents = []
    async with http_get(data["url"]) as r:
        res = await r.text()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res, "html.parser")
        find = soup.find("div", class_="post-body entry-content")
        find_all = find.find_all("p")
        for p in find_all:
            if p.string:
                contents.append(p.string)

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
    novels = []
    if len(sys.argv) < 2 or not sys.argv[1] == "clean":
        # 读取任务队列
        novels = load_json(DATA_PATH + "/tasks.json")
    if len(novels) <= 0:
        novels = await get_novels_list()
    print(f"开始采集，共计{len(novels)}本")
    success = []
    for novel in novels:
        chapters = await get_novel_chapters(novel)
        print(f"正在采集[{novel['title']}]，共{len(chapters)}章")
        tasks = []
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        from tqdm.asyncio import tqdm
        pbar = tqdm(total=len(chapters), desc=novel["title"], ascii=True)
        for chapter in chapters:
            tasks.append(asyncio.create_task(semap(semaphore, collect_contents, chapter,
                                                   lambda x: pbar.update(1) and pbar.set_description(x["title"]))))
        await asyncio.wait(tasks)
        pbar.close()
        chapter_contents = ''
        for k in range(len(tasks)):
            chapter_contents += chapters[k]['title'] + "\n\n" + tasks[k].result() + "\n\n"
        save(OUPUT, novel['title'], chapter_contents.strip("\n"))
        print(f"[{novel['title']}]采集完毕，共{len(chapters)}章")
        success.append(novel)
        save(DATA_PATH, 'tasks', json.dumps([val for val in novels if val not in success], ensure_ascii=False), '.json')
    print(f"采集完毕，共计{len(novels)}本，成功{len(success)}本，失败{len(novels) - len(success)}")


OUPUT = "./output"
DATA_PATH = "./"
# 并行数
MAX_WORKERS = 10
# http代理
PROXY = ''

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

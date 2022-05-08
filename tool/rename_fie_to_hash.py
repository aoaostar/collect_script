# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/19
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import asyncio
import hashlib
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor

from tqdm import tqdm


def sha1(filepath):
    hash = hashlib.sha1()
    with open(filepath, "rb") as f:
        while True:
            b = f.read(2048)
            if not b:
                break
            hash.update(b)
    return hash.hexdigest()


def process(file):
    bar.set_description(os.path.basename(file))
    filename = sha1(file) + file[file.rindex('.'):]
    os.rename(file, os.path.dirname(file) + '/' + filename)
    bar.update(1)


async def main():
    async with asyncio.Semaphore(10):
        await asyncio.gather(*[process(file) for file in list_files])


async def main2():
    await asyncio.gather(*[process(file) for file in list_files])


MERGE_PATH = './images'
list_files = []
bar = tqdm(total=len(list_files))

for root, dirs, files in os.walk(MERGE_PATH):
    for name in files:
        list_files.append(os.path.join(root, name))
# 开始
now = time.time()
bar.reset(total=len(list_files))
with ThreadPoolExecutor(max_workers=10) as p:
    p.map(process, list_files)

print(f"多线程执行完毕，耗时{time.time() - now}s")

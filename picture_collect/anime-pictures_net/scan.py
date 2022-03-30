# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/3/30
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------

import json
import os
import re


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


if __name__ == '__main__':
    print("正在扫描空白页（未采集成功的）")
    path = './data'
    listdir = os.listdir(path)
    empty_list = []
    for dir in listdir:
        data = load_json(path + '/' + dir)
        if len(data) <= 0:
            empty_list.append(re.findall('\d+', dir)[0])
    print(f"扫描完毕，共{len(empty_list)}页为空")
    print(empty_list)

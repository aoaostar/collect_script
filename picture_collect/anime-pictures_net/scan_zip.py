# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/21
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import os

listdir = os.listdir('./package')

arr = []
for file in listdir:

    if os.path.getsize('./package/' + file) < 10240:
        arr.append(f"https://drive.aoaostar.com/d/700G_二次元/700G_二次元_打包/{file}")

print("\n".join(arr))

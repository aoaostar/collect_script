# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/19
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import os

MERGE_PATH = './images'
list_files = []
list_dirs = []
for root, dirs, files in os.walk(MERGE_PATH):
    for name in files:
        list_files.append(os.path.join(root, name))

    for name in dirs:
        list_dirs.append(os.path.join(root, name))

for file in list_files:

    os.rename(file, MERGE_PATH + '/' +os.path.basename(file))

for dir in list_dirs:
    os.removedirs(dir)

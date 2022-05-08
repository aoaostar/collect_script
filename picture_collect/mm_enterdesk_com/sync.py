# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/9
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import subprocess

PACKAGE_PATH = "./回车桌面原图"
ONDRIVE_REMOTE_PATH = "one:alist/回车桌面"

def run_cmd(commands):
    print("commands:", commands)
    subprocess_run = subprocess.run(commands, shell=True)
    return subprocess_run.returncode == 0


run_cmd(f'zip -q 回车桌面打包.zip README.md')
run_cmd(f'cd {PACKAGE_PATH} && zip -rq ../回车桌面打包.zip ./* && cd ../')
run_cmd(f'rclone copy -cv 回车桌面打包.zip {ONDRIVE_REMOTE_PATH}')
run_cmd(f'rclone copy -cv --transfers=20 {PACKAGE_PATH} {ONDRIVE_REMOTE_PATH}/回车桌面原图')

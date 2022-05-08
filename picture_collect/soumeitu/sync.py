# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/9
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import subprocess

PACKAGE_PATH = "./搜美图"
ONDRIVE_REMOTE_PATH = "one:alist/搜美图"


def run_cmd(commands):
    print("commands:", commands)
    subprocess_run = subprocess.run(commands, shell=True)
    return subprocess_run.returncode == 0


run_cmd(f'rclone copy -cvP ./搜美图打包.zip {ONDRIVE_REMOTE_PATH}')
run_cmd(f'rclone copy -cvP --transfers=20 {PACKAGE_PATH} {ONDRIVE_REMOTE_PATH}/原图')
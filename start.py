# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os

from tools.docker_api import DockerApi

docker = DockerApi.from_env()


def start_rpc_server():
    print("正在启动rpc服务...")
    os.system("docker rm -f server-rpc")
    os.system(
        'docker run -itd --name server-rpc -p 9005:9005 --network net_center -e HOST="0.0.0.0" -e PORT=9005 -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker server-rpc')


def start_web_server():
    print("正在启动web服务... ...")
    os.system("docker rm -f server-web")
    os.system("docker run -itd --name server-web -p 9006:8000 server-web")


tasks = [
    {
        "name": "启动RPC服务",
        "func": start_rpc_server
    },
    {
        "name": "启动Web服务",
        "func": start_web_server
    },
]

if __name__ == '__main__':
    print("启动服务... ...")

    for i, task in enumerate(tasks):
        print(f"[{i + 1}]: {task['name']}")

    try:
        i = input()
        tasks[int(i) - 1]["func"]()
    except Exception as e:
        print("error input,exit")
        exit()

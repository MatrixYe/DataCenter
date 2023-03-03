# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as log
import os

from tools.docker_api import DockerApi

docker = DockerApi.from_env()

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


def start_rpc_server():
    log.info("正在启动rpc服务... ...")
    cmd1 = 'docker rm -f server-rpc'
    c_name = 'server-rpc'
    c_port = '9005:9005'
    c_network = 'net_center'
    c_volume = '/var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker'
    c_img = 'server-rpc'
    c_e_host = 'HOST="0.0.0.0"'
    c_e_port = '9005'
    cmd2 = f'docker run -itd --name {c_name} -p {c_port} --network {c_network} -e {c_e_host} -e PORT={c_e_port} -v {c_volume} {c_img}'
    os.system(cmd1)
    os.system(cmd2)


def start_web_server():
    log.info("正在启动HTTP服务... ...")
    cmd1 = 'docker rm -f server-http'
    c_name = 'server-http'
    c_port = '9006:9006'
    c_network = 'net_center'
    c_volume = '/var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker'
    c_img = 'server-http'
    c_e_host = 'HOST="0.0.0.0"'
    c_e_port = '9006'
    cmd2 = f'docker run -itd --name {c_name} -p {c_port} --network {c_network} -e {c_e_host} -e PORT={c_e_port} -v {c_volume} {c_img}'
    log.info(cmd2)
    os.system(cmd1)
    os.system(cmd2)


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

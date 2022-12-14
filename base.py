# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os
from tools import config, docker


def start_postgres(c):
    name = c['name']
    port = c['port']
    name = c['name']
    volume = c['volume']
    network = c['network']
    network_alias = c['network-alias']
    user = c['user']
    password = c['password']
    restart = c['restart']
    img = c['img']

    docker.pull_image(img)
    docker.create_network(network)
    docker.create_volume(volume)
    docker.run_pg_container(name, port, network, network_alias, volume, user, password, restart, img)


def start_redis(c):
    name = c["name"]
    port = c["port"]
    volume = c["volume"]
    network = c["network"]
    network_alias = c["network-alias"]
    password = c["password"]
    restart = c["restart"]
    img = c["img"]

    docker.create_volume(volume)
    docker.create_network(network)
    docker.pull_image(img)
    docker.run_redis_container(name, port, network, network_alias, volume, restart, img, password)


if __name__ == '__main__':
    print("---------- START ----------")
    os.system('pip install -r requirements.txt')
    docker.pull_image('python:latest')
    data = config.load_config()
    start_redis(data['redis']['docker'])
    start_postgres(data['postgres']['docker'])
    print(docker.get_container(True))
    print("----------- END -----------")

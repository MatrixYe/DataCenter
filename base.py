# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import warnings

from tools.docker_api import DockerApi
from utils import load_config

docker_api = DockerApi.from_env()


def start_redis(c):
    """
    启动并初始化本地redis 容器
    :param c:
    :return:
    """
    name = c["name"]
    port = c["port"]
    volume = c["volume"]
    network = c["network"]
    network_alias = c["network-alias"]
    password = c["password"]
    restart = c["restart"]
    img = c["img"]

    docker_api.create_volume(volume)
    docker_api.create_network(network)
    docker_api.pull_image(img)
    docker_api.run_redis_container(name, port, network, network_alias, volume, restart, img, password)


def start_postgres(c):
    warnings.warn("postgres database 已废弃", DeprecationWarning)
    name = c['name']
    port = c['port']
    volume = c['volume']
    network = c['network']
    network_alias = c['network-alias']
    user = c['user']
    password = c['password']
    restart = c['restart']
    img = c['img']

    docker_api.pull_image(img)
    docker_api.create_network(network)
    docker_api.create_volume(volume)
    docker_api.run_pg_container(name, port, network, network_alias, volume, user, password, restart, img)


def start_mongo(c):
    name = c['name']
    port = c['port']
    volume = c['volume']
    network = c['network']
    network_alias = c['network-alias']
    user = c['user']
    password = c['password']
    restart = c['restart']
    img = c['img']
    cache = c['cache']
    memory = c['memory']
    memory_swap = c['memory_swap']

    docker_api.pull_image(img)
    docker_api.create_network(network)
    docker_api.create_volume(volume)
    docker_api.run_mongo_container(name, port, network, network_alias, volume, user, password, restart, img, cache,
                                   memory, memory_swap)


if __name__ == '__main__':
    print("---------- START ----------")
    # os.system('pip install -r requirements.txt')
    print("正在加载python1.0镜像... ...")
    docker_api.pull_image('python:3.10')
    print("正在加载系统配置... ...")
    conf = load_config()
    print("正在启动redis docker容器... ...")
    start_redis(c=conf['redis']['docker'])
    # start_postgres(conf['postgres']['docker']) # 废除PG数据库
    print("正在mongodb docker 容器... ...")
    start_mongo(c=conf['mongo']['docker'])
    print(docker_api.continers(True))
    print("----------- END -----------")

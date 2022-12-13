# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import docker
import json
import os

client = docker.from_env()


# 获取docker镜像列表
def get_images() -> list:
    result = list()
    images_arr = [a.tags for a in client.images.list()]
    for buff in images_arr:
        for image in buff:
            result.append(image)
    return result


# 获取docker网络列表
def get_network() -> list:
    return [a.name for a in client.networks.list()]


# 获取docker挂载列表
def get_volume() -> list:
    return [a.name for a in client.volumes.list()]


# 获取docker容器列表
def get_container(flag=False) -> list:
    return [a.name for a in client.containers.list(all=flag)]


# 拉取docker镜像
def pull_image(img_name: str):
    if img_name not in get_images():
        print(f"---> pull image:{img_name}")
        os.system(f"docker pull {img_name}")
    else:
        print(f"image:{img_name} is exited --> pass")


# 创建docker挂载
def create_volume(name: str) -> None:
    # create volume
    if name not in get_volume():
        print(f"---> create volume :{name}")
        client.volumes.create(name)
    else:
        print(f"volume:{name} is exited --> pass")


# 创建docker网络
def create_network(name: str):
    if name not in get_network():
        print(f"---> create network:{name}")
        client.networks.create(name)
    else:
        print(f"network:{name} is exited --> pass")


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

    pull_image(img)
    create_network(network)
    create_volume(volume)
    if name not in get_container(flag=False):
        if name in get_container(True):
            os.system(f"docker rm {name}")
            print(f"container:{name} is exist and is stopped --> remove")
        cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -v {volume}:/var/lib/postgresql/data -e POSTGRES_USER={user} -e POSTGRES_PASSWORD={password} -e ALLOW_IP_RANGE=0.0.0.0/0 --restart={restart} {img}"
        print(f"指令: {cmd}")
        os.system(cmd)
    else:
        print(f"container:{name} is exist and is running --> pass")


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def start_redis(config):
    name = config["name"]
    port = config["port"]
    volume = config["volume"]
    network = config["network"]
    network_alias = config["network-alias"]
    password = config["password"]
    restart = config["restart"]
    img = config["img"]

    create_volume(volume)
    create_network(network)
    pull_image(img)

    if name not in get_container(flag=False):
        if name in get_container(True):
            os.system(f"docker rm {name}")
            print(f"container:{name} is exist bud not run --> remove it")
        cmd = f"docker run -itd -p {port} --name {name} --network {network} --network-alias {network_alias} -v {volume}:/data --restart={restart} {img} --requirepass {password} "
        print(f"指令: {cmd}")
        os.system(cmd)
    else:
        print(f"container:{name} is exist and is running --> pass")


if __name__ == '__main__':
    print("---------- START ----------")
    os.system('pip install -r requirements.txt')
    pull_image("python:latest")
    data = load_config()
    start_redis(data['redis']['docker'])
    start_postgres(data['postgres']['docker'])
    print("----------- END -----------")

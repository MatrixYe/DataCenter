# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os

import docker

client = docker.from_env()


# 获取docker镜像列表
def images() -> list:
    result = list()
    # 二级数组
    groups = [a.tags for a in client.images.list()]
    for group in groups:
        for image in group:
            result.append(image)
    return result


# 获取docker网络列表
def networks() -> list:
    return [a.name for a in client.networks.list()]


# 获取docker挂载列表
def volumes() -> list:
    return [a.name for a in client.volumes.list()]


# 获取docker容器列表
def continers(flag=False) -> list:
    return [a.name for a in client.containers.list(all=flag)]


def statu(c_name: str) -> int:
    # - `status` (str): One of ``restarting``, ``running``,
    #                     ``paused``, ``exited``
    cs = client.containers.list(all=True)
    for c in cs:
        if c.name == c_name and c.status == 'running':
            return 1
        if c.name == c_name and c.status != 'running':
            return -1
    return 0


# 拉取docker镜像
def pull_image(img_name: str):
    if img_name not in images():
        print(f"---> pull image:{img_name}")
        client.images.pull(img_name)
    else:
        print(f"image:{img_name} is exited --> pass")


def rm_image(img_name: str, force: bool):
    imgs = images()
    for _, img in enumerate(imgs):
        if img == img_name:
            img.remove(force=force)
            return
    print(f"image:{img_name} is not find ")


def rm_container(name, force: bool):
    cs = client.containers.list(all=True)
    for i, c in enumerate(cs):
        if c.name == name or c.short_id == name:
            print(f"find container:{c.name} --> remove it")
            c.remove(force=force)
            return
    print(f"container:{name} is not finded")


# 创建docker挂载
def create_volume(name: str):
    # create volume
    if name not in volumes():
        print(f"volume :{name} --> creating")
        client.volumes.create(name)
    else:
        print(f"volume:{name} is exited --> pass")


# 创建docker网络
def create_network(name: str):
    if name not in networks():
        print(f"network:{name} --> creating")
        client.networks.create(name)
    else:
        print(f"network:{name} is exited --> pass")


# 创建并运行redis容器
def run_redis_container(name, port, network, network_alias, volume, restart, img, password):
    if name not in continers(flag=False):
        if name in continers(True):
            print(f"container:{name} is exist bud not run --> remove it")
            os.system(f"docker rm {name}")
        print(f"container{name} --> creating")
        cmd = f"docker run -itd -p {port} --name {name} --network {network} --network-alias {network_alias} -v {volume}:/data --restart={restart} {img} --requirepass {password} "
        print(f"CMD: {cmd}")
        os.system(cmd)
    else:
        print(f"container:{name} is exist and is running --> pass")


# 创建并运行postgrest容器
def run_pg_container(name, port, network, network_alias, volume, user, password, restart, img):
    if name not in continers(flag=False):
        if name in continers(True):
            os.system(f"docker rm {name}")
            print(f"container:{name} is exist and is stopped --> remove")
        print(f"container{name} --> creating")
        cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -v {volume}:/var/lib/postgresql/data -e POSTGRES_USER={user} -e POSTGRES_PASSWORD={password} -e ALLOW_IP_RANGE=0.0.0.0/0 --restart={restart} {img}"
        print(f"CMD: {cmd}")
        os.system(cmd)
    else:
        print(f"container:{name} is exist and is running --> pass")


# 创建并运行mongodb容器
def run_mongo_container(name, port, network, network_alias, volume, user, password, restart, img, cache, memory,
                        memory_swap):
    if name not in continers(flag=False):
        if name in continers(True):
            os.system(f"docker rm {name}")
            print(f"container:{name} is exist and is stopped --> remove")
        print(f"container:{name} --> creating")
        cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -m {memory} --memory-swap {memory_swap} -e MONGO_INITDB_ROOT_USERNAME={user} -e MONGO_INITDB_ROOT_PASSWORD={password} -v {volume}:/data/db {img} --wiredTigerCacheSizeGB {cache}"
        print(f"CMD: {cmd}")
        os.system(cmd)
    else:
        print(f"container:{name} is exist and is running --> pass")


def run_hello_world():
    pass

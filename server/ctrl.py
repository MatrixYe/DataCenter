# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os

import uitls
from tools.docker_api import DockerApi

docker_api = DockerApi.from_env()


def run_sync_block_container(network: str, origin: int, interval: int, node: str, reload: bool):
    net = uitls.load_docker_net()
    name = f"block-{network}"
    net_alias = f"{name}host"
    img = "sync-block:latest"
    restart = "always"
    st = docker_api.statu(name)
    if st == 0:
        print("container is not exist --> creating")
        cmd = f'docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE="{node}" -e RELOAD={reload} --network {net} --network-alias {net_alias} --restart={restart} {img}'
        print(cmd)
        os.system(cmd)
        return f"container({name}) is not exist --> creating"
    if st == 1:
        print("container is exist --> pass")
        return f"container({name}) is  exist --> PASS"

    if st == -1:
        print("container is exist,but not running --> remove and creating")
        cmd1 = f"docker rm -f {name}"
        cmd2 = f'docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE="{node}" -e RELOAD={reload} --network {net} --network-alias {net_alias} --restart={restart} {img}'
        os.system(cmd1)
        os.system(cmd2)
        return f"container({name}) is exist,but not running -->  remove and creating"


def rm_sync_block_container(network: str):
    name = f"block-{network}"
    st = docker_api.statu(name)
    if st == 0:
        print(f"container:{name} is not exist --> pass")
        return f"container:{name} is not exist --> PASS"
    if st == 1:
        print(f"container:{name} is  exist and running --> stop&remove")
        # cmd1 = f"docker stop {name}"
        cmd2 = f"docker rm -f {name}"
        # os.system(cmd1)
        os.system(cmd2)
        return f"container:{name} is exist and running --> stop&remove"
    if st == -1:
        print(f"container:{name} is exist and stoped --> remove")
        cmd = f"docker rm -f {name}"
        os.system(cmd)
        return f"container:{name} is  exist and running --> stop&remove"


def run_sync_event_container(network: str, target: str, origin: int, node: str, reload: bool, delay: int, ranger: int):
    net = uitls.load_docker_net()
    name = f"event-{target[2:6]}-{target[-4:]}"
    net_alias = f"{name}host"
    img = "sync-event:latest"
    restart = "always"
    st = docker_api.statu(name)
    if st == 0:
        print("container is not exist --> creating")
        cmd = f'docker run -itd --name {name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e RELOAD={reload} -e DELAY={delay} -e RANGE={ranger} --network {net} --network-alias {net_alias} --restart={restart} {img}'
        print(cmd)
        os.system(cmd)
        return f"container({name}) is not exist --> creating"
    if st == 1:
        print("container is exist --> pass")
        return f"container({name}) is  exist --> PASS"

    if st == -1:
        print("container is exist,but not running --> remove and creating")
        cmd1 = f"docker rm -f {name}"
        cmd2 = f'docker run -itd --name {name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e RELOAD={reload} -e DELAY={delay} -e RANGE={ranger} --network {net} --network-alias {net_alias} --restart={restart} {img}'
        os.system(cmd1)
        os.system(cmd2)
        return f"container({name}) is exist,but not running -->  remove and creating"


def rm_sync_event_container(target: str):
    name = f"event-{target[2:6]}-{target[-4:]}"
    st = docker_api.statu(name)
    if st == 0:
        print(f"container:{name} is not exist --> pass")
        return f"container:{name} is not exist --> PASS"
    if st == 1:
        print(f"container:{name} is  exist and running --> stop&remove")
        # cmd1 = f"docker stop {name}"
        cmd2 = f"docker rm -f {name}"
        # os.system(cmd1)
        os.system(cmd2)
        return f"container:{name} is exist and running --> stop&remove"
    if st == -1:
        print(f"container:{name} is exist and stoped --> remove")
        cmd = f"docker rm -f {name}"
        os.system(cmd)
        return f"container:{name} is  exist and running --> stop&remove"

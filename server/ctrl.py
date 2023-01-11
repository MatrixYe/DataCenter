# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os

import utils
from tools.docker_api import DockerApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi

IMG_SYNC_EVENT = "sync-event:latest"
IMG_SYNC_BLOCK = "sync-block:latest"
IMG_SYNC_ORACLE = "sync_oracle:latest"


class Ctrl(object):
    def __init__(self, docker: DockerApi, redis: RedisApi, mongo: MongoApi):
        assert docker is not None, "docker is None,can not init Ctrl class"
        assert redis is not None, "redis is None,can not init Ctrl class"
        assert mongo is not None, "mongo is None,can not init Ctrl class"
        self.docker = docker
        self.redis = redis
        self.mongo = mongo

    # 新增同步block链,运行容器
    def start_sync_block(self, network: str, origin: int, interval: int, node: str, webhook: str):
        net = utils.load_docker_net()
        name = utils.gen_block_continal_name(network=network)
        net_alias = utils.gen_docker_net_alias(contailer_name=name)
        img = IMG_SYNC_BLOCK
        restart = "on-failure:3"
        st = self.docker.statu(name)
        if st == 0:
            print("container is not exist --> creating")
            cmd = f'docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE="{node}" -e WEBHOOK={webhook} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            print(cmd)
            os.system(cmd)
            return f"container({name}) is not exist --> creating"
        if st == 1:
            print("container is exist --> pass")
            return f"container({name}) is  exist --> PASS"

        if st == -1:
            print("container is exist,but not running --> remove and creating")
            cmd1 = f"docker rm -f {name}"
            cmd2 = f'docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE="{node}" -e WEBHOOK={webhook} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            os.system(cmd1)
            os.system(cmd2)
            print(cmd1)
            print(cmd2)

            return f"container({name}) is exist,but not running -->  remove and creating"

    # 停止同步block data
    def stop_sync_block(self, network: str, delete: bool):
        container_name = utils.gen_block_continal_name(network)
        table_name = utils.gen_block_table_name(network=network)
        cache_name = utils.gen_block_cache_name(network=network)
        st = self.docker.statu(container_name)
        # 容器不存在 --> 创建
        if st == 0:
            print(f"container:{container_name} is not exist --> pass")
            return f"container:{container_name} is not exist --> PASS"
        # 容器已经存在，运行中 --> 停止且移除
        if st == 1:
            print(f"container:{container_name} is  exist and running --> stop&remove")
            # cmd1 = f"docker stop {name}"
            cmd2 = f"docker rm -f {container_name}"
            # os.system(cmd1)
            os.system(cmd2)
            return f"container:{container_name} is exist and running --> stop&remove"
        # 容器已存在,但停止 --> 移除
        if st == -1:
            print(f"container:{container_name} is exist and stoped --> remove")
            cmd = f"docker rm -f {container_name}"
            os.system(cmd)
            return f"container:{container_name} is  exist and running --> stop&remove"
        if delete:
            self.mongo.drop(table_name)
            self.redis.delele(cache_name)

    # 开始同步event out 数据
    def start_sync_event(self, network: str, target: str, origin: int, node: str, delay: int, ranger: int,
                         webhook: str):
        net = utils.load_docker_net()
        container_name = utils.gen_event_container_name(network, target)
        net_alias = utils.gen_docker_net_alias(contailer_name=container_name)
        img = IMG_SYNC_EVENT
        restart = "on-failure:3"
        st = self.docker.statu(container_name)
        if st == 0:
            print("container is not exist --> creating")
            cmd = f'docker run -itd --name {container_name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e WEBHOOK="{webhook}" -e DELAY={delay} -e RANGE={ranger} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            print(cmd)
            os.system(cmd)
            return f"container({container_name}) is not exist --> creating"
        if st == 1:
            print("container is exist --> pass")
            return f"container({container_name}) is  exist --> PASS"

        if st == -1:
            print("container is exist,but not running --> remove and creating")
            cmd1 = f"docker rm -f {container_name}"
            cmd2 = f'docker run -itd --name {container_name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e WEBHOOK={webhook} -e DELAY={delay} -e RANGE={ranger} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            os.system(cmd1)
            os.system(cmd2)
            print(cmd1)
            print(cmd2)
            return f"container({container_name}) is exist,but not running -->  remove and creating"

    # 停止同步event数据
    def stop_sync_event(self, network: str, target: str, delete: bool):
        container_name = utils.gen_event_container_name(network=network, target=target)
        table_name = utils.gen_event_table_name(network=network, target=target)
        cache_name = utils.gen_event_cache_name(network=network, target=target)
        st = self.docker.statu(container_name)
        if st == 0:
            print(f"container:{container_name} is not exist --> pass")
            return f"container:{container_name} is not exist --> PASS"
        if st == 1:
            print(f"container:{container_name} is  exist and running --> stop&remove")
            # cmd1 = f"docker stop {container_name}"
            cmd2 = f"docker rm -f {container_name}"
            # os.system(cmd1)
            os.system(cmd2)
            return f"container:{container_name} is exist and running --> stop&remove"
        if st == -1:
            print(f"container:{container_name} is exist and stoped --> remove")
            cmd = f"docker rm -f {container_name}"
            os.system(cmd)
            return f"container:{container_name} is  exist and running --> stop&remove"
        if delete:
            print("删除event数据及缓存")
            self.mongo.drop(table_name)
            self.redis.delele(cache_name)

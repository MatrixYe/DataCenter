# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: RPC服务- 控制工具类
# -------------------------------------------------------------------------------
import os

import utils
from tools.docker_api import DockerApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi

IMG_SYNC_EVENT = "sync-event:latest"
IMG_SYNC_BLOCK = "sync-block:latest"
IMG_SYNC_ORACLE = "sync-oracle:latest"


class Ctrl(object):
    def __init__(self, docker: DockerApi, redis: RedisApi, mongo: MongoApi):
        assert docker is not None, "docker is None,can not init Ctrl"
        assert redis is not None, "redis is None,can not init Ctrl"
        assert mongo is not None, "mongo is None,can not init Ctrl"
        self.docker = docker
        self.redis = redis
        self.mongo = mongo

    def start_sync_block(self, network: str, origin: int, interval: int, node: str, webhook: str):
        """
        新增同步block链,运行容器
        :param network:
        :param origin:
        :param interval:
        :param node:
        :param webhook:
        :return:
        """
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
        """
        停止block 同步
        :param network: 需要停止的网络
        :param delete:
        :return:
        """
        container_name = utils.gen_block_continal_name(network)
        table_name = utils.gen_block_table_name(network=network)
        tag_block = utils.gen_block_tag(network=network)
        st = self.docker.statu(container_name)
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
            self.redis.delele(tag_block)

    # 开始同步event out 数据
    def start_sync_event(self, network: str, target: str, origin: int, node: str, delay: int, range: int,
                         webhook: str):
        net = utils.load_docker_net()
        container_name = utils.gen_event_container_name(network, target)
        net_alias = utils.gen_docker_net_alias(contailer_name=container_name)
        img = IMG_SYNC_EVENT
        restart = "on-failure:3"
        st = self.docker.statu(container_name)
        if st == 0:
            print("container is not exist --> creating")
            cmd = f'docker run -itd --name {container_name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e WEBHOOK="{webhook}" -e DELAY={delay} -e RANGE={range} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            print(cmd)
            os.system(cmd)
            return f"container({container_name}) is not exist --> creating"
        if st == 1:
            print("container is exist --> pass")
            return f"container({container_name}) is  exist --> PASS"

        if st == -1:
            print("container is exist,but not running --> remove and creating")
            cmd1 = f"docker rm -f {container_name}"
            cmd2 = f'docker run -itd --name {container_name} -e NETWORK={network} -e TARGET={target} -e ORIGIN={origin} -e NODE="{node}" -e WEBHOOK={webhook} -e DELAY={delay} -e RANGE={range} --network {net} --network-alias {net_alias} --restart={restart} {img}'
            os.system(cmd1)
            os.system(cmd2)
            print(cmd1)
            print(cmd2)
            return f"container({container_name}) is exist,but not running -->  remove and creating"

    # 停止同步event数据
    def stop_sync_event(self, network: str, target: str, delete: bool) -> str:

        container_name = utils.gen_event_container_name(network=network, target=target)
        table_name = utils.gen_event_table_name(network=network, target=target)
        tag_event = utils.gen_event_tag(network=network, target=target)
        st = self.docker.statu(container_name)
        msg = "done"
        if st == 0:
            print(f"container:{container_name} is not exist --> pass")
            msg = f"container:{container_name} is not exist --> PASS"
        if st == 1:
            print(f"container:{container_name} is exist and running --> stop&remove")
            # cmd1 = f"docker stop {container_name}"
            cmd2 = f"docker rm -f {container_name}"
            # os.system(cmd1)
            print(cmd2)
            os.system(cmd2)
            msg = f"container:{container_name} is exist and running --> stop&remove"
        if st == -1:
            print(f"container:{container_name} is exist and stoped --> remove")
            cmd = f"docker rm -f {container_name}"
            os.system(cmd)
            msg = f"container:{container_name} is  exist and running --> stop&remove"
        if delete:
            print("删除event数据及缓存")
            self.mongo.drop(table_name)
            self.redis.delele(tag_event)
        return msg

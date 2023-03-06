# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from typing import Union

from docker.models.containers import Container

import utils
from .docker_api import DockerApi
from .mongo_api import MongoApi
from .redis_api import RedisApi

IMG_SYNC_EVENT = "sync-event:latest"
IMG_SYNC_BLOCK = "sync-block:latest"
IMG_SYNC_ORACLE = "sync-oracle:latest"


class _Ctrl(object):
    def _conn_redis(self) -> RedisApi:
        """
        连接redis
        :return: redis client
        """
        redis_conf = self.conf['redis']['outside'] if utils.is_dev_env() else self.conf['redis']['inside']
        return RedisApi.from_config(**redis_conf)

    def _conn_mongo(self) -> MongoApi:
        """
        连接mongo
        :return: mongodb client
        """
        c = self.conf['mongo']['outside'] if utils.is_dev_env() else self.conf['mongo']['inside']
        return MongoApi.from_conf(**c)

    # noinspection PyMethodMayBeStatic
    def _conn_docker(self) -> DockerApi:
        """
        连接docker control
        :return: docker client
        """
        return DockerApi.from_env()

    def __init__(self, conf: dict):
        self.conf = conf
        self.docker: DockerApi = self._conn_docker()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()


class BlockCtrl(_Ctrl):
    def __init__(self, conf):
        super().__init__(conf)

    def _start_sync_block(self, c_name, c_net, c_env, c_restart) -> Union[Container, None]:
        container = self.docker.run_container(image=IMG_SYNC_BLOCK,
                                              name=c_name,
                                              network=c_net,
                                              volumes=None,
                                              ports=None,
                                              environment=c_env, restart=c_restart, commond=None)
        return container

    # 开始同步block区块高度
    def start_block(self, network: str, origin: int, interval: int, node: str, webhook: str,
                    restart: bool = False) -> (Container, str):
        """
        新增同步block链,运行容器
        :param restart:
        :param network:
        :param origin:
        :param interval:
        :param node:
        :param webhook:
        :return:
        """
        c_net = utils.load_docker_net()
        c_name = utils.gen_block_continal_name(network=network)
        # c_restart = {"Name": "on-failure", "MaximumRetryCount": 3}
        c_restart = {"Name": "always"}
        c_env = {
            "NETWORK": network,
            "ORIGIN": origin,
            "INTERVAL": interval,
            "NODE": node,
            "WEBHOOK": webhook,
        }

        old_container = self.docker.get_container(c_name)
        # 容器不存在->创建
        if old_container is None:
            print("container is not exist --> creating")
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            return (new_container, 'create') if new_container else (None, 'failed')
        # 容器存在+重启->移除&创建
        if old_container and restart:
            self.remove_block(network, delete=False)
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            return (new_container, 'remove&retart&create') if new_container else (None, 'failed')
        # 容器存在+运行状态+不重启 -> 跳过
        if old_container and old_container.status == 'running':
            return old_container, 'pass'
        # 容器存在+停止状态+不重启 -> 移除+创建
        if old_container and old_container.status != 'running':
            self.remove_block(network, delete=False)
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            return (new_container, 'remove&create') if new_container else (None, 'failed')
        return None, 'unknow'

    # 停止同步block data
    def remove_block(self, network: str, delete: bool) -> (str, str):
        """
        停止block 同步
        :param network: 需要停止的网络
        :param delete:
        :return:
        """
        container_name = utils.gen_block_continal_name(network)
        table_name = utils.gen_block_table_name(network=network)
        tag_block = utils.gen_block_tag(network=network)
        container = self.docker.get_container(container_name)
        if container is None:
            return container_name, 'noexist&pass'
        _, _ = self.docker.remove_container(container_name, force=True)

        if delete:
            self.mongo.drop(table_name)
            self.redis.delele(tag_block)
            return container_name, 'remove&clear'
        return container_name, 'remove'

    # 获取最新同步的block高度
    def last_block(self, network) -> Union[dict, None]:
        tag = utils.gen_block_tag(network)
        return self.redis.getdict(tag)


class EventCtrl(_Ctrl):
    def __init__(self, conf):
        super().__init__(conf)

    def start_event(self):
        pass

    def remove_event(self):
        pass

    def restart_event(self):
        pass

    pass

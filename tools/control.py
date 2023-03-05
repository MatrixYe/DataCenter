# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

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

    def start_sync_block(self, network: str, origin: int, interval: int, node: str, webhook: str) -> (str, str):
        """
        新增同步block链,运行容器
        :param network:
        :param origin:
        :param interval:
        :param node:
        :param webhook:
        :return:
        """
        c_net = utils.load_docker_net()
        c_name = utils.gen_block_continal_name(network=network)
        c_restart = {"Name": "on-failure", "MaximumRetryCount": 3}
        c_evn = {
            "NETWORK": network,
            "ORIGIN": origin,
            "INTERVAL": interval,
            "NODE": node,
            "WEBHOOK": webhook,
        }

        container = self.docker.get_container(c_name)
        if container is None:
            print("container is not exist --> creating")
            container = self.docker.run_container(image=IMG_SYNC_BLOCK, name=c_name, network=c_net,
                                                  volumes=None,
                                                  ports=None,
                                                  environment=c_evn, restart=c_restart, commond=None)
            if not container:
                return 'failed', 'failed'
            return container.name, 'create'

        elif container.status == 'running':
            return container.name, 'pass'
        else:
            self.docker.remove_container(c_name, True)
            container = self.docker.run_container(image=IMG_SYNC_BLOCK, name=c_name, network=c_net,
                                                  volumes=None,
                                                  ports=None,
                                                  environment=c_evn, restart=c_restart, commond=None)
            return container.name, 'remove&create'

    # 停止同步block data
    def stop_sync_block(self, network: str, delete: bool) -> (str, str):
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

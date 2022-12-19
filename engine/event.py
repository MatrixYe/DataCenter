# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as log
import time
from tools.eth_api import EthApi
from tools.redis_api import RedisApi
from tools.mongo_api import MongoApi
from uitls import is_dev_env

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


class Task(object):
    def __init__(self, conf, **kwargs):
        self.conf: dict = conf
        self.network = kwargs.get("network").lower()
        self.target = kwargs.get("target")
        self.origin = kwargs.get("origin")
        self.node = kwargs.get("node")
        self.reload = kwargs.get("reload")
        #
        self.eth: EthApi = self._conn_eth()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()
        if not self.eth.is_address(self.target):
            log.error(f"event out target:{self.target} is not a right address ")
            exit()
        self.tag_height = f"event_{self.target[2:6]}_{self.target[-4:]}"
        self.tag_block_height = f"block_{self.network}_height"
        self.table_name = f"event_{self.target[2:6]}_{self.target[-4:]}"  # evet-77ba-ab12

    def run(self):
        log.info(
            f"sync event:network:{self.network} target:{self.target} origin:{self.origin} reload:{self.reload} node:{self.node}")
        if self.reload:
            self.clear_all()

        while True:
            time.sleep(2)
            x = self.local_height()
            y = self.remote_height()
            log.info(f"x={x} y={y}")
            if y == 0:
                log.warning("block height is Zero,please check network")
                continue
            if x == 0:
                x = self.origin if self.origin else y - 3
            if y <= x:
                continue

    def local_height(self) -> int:
        h = self.redis.get(self.tag_height)
        if h is None:
            return 0
        else:
            return int(h)

    def remote_height(self) -> int:
        h = self.redis.get(self.tag_block_height)
        if h is None:
            return 0
        else:
            return int(h)

    def _conn_redis(self) -> RedisApi:
        c = self.conf
        if is_dev_env():
            return RedisApi.from_config(**c['redis']['outside'])
        else:
            return RedisApi.from_config(**c['redis']['inside'])

    def _conn_mongo(self) -> MongoApi:
        c = self.conf
        if is_dev_env():
            return MongoApi.from_conf(**c['mongo']['outside'])
        else:
            return MongoApi.from_conf(**c['mongo']['inside'])

    def _conn_eth(self) -> EthApi:
        return EthApi.from_node(self.node)

    def clear_all(self):
        log.info("clear all data in mongo ,and clear redis tag")
        # 1.清除database
        self.mongo.drop(self.table_name)
        # 2.清除fredi标识
        self.redis.delele(self.tag_height)

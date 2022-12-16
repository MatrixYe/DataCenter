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
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from uitls import is_dev_env

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


class Task(object):
    def __init__(self, conf, **kwargs):
        self.network: str = kwargs.get("network")
        self.interval: int = kwargs.get("interval")
        self.origin: int = kwargs.get("origin")
        self.node: str = kwargs.get("node")
        self.reload: bool = kwargs.get("reload")
        self.conf: dict = conf
        self.eth: EthApi = self._conn_eth()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()
        self.tag_height = f"block-{self.network}-height"
        self.tag_timestamp = f"block-{self.network}-timestamp"
        self.collection = f"block-{self.network}"

    def run(self):
        log.debug(f"sync block:network:{self.network} origin:{self.origin} reload:{self.reload} node:{self.node}")
        # print(self.mongo.add_test_data({'name': 'wangdachui', 'age': 30}))
        while True:
            time.sleep(self.interval)
            print("开始同步block数据")
            x = self.local_height()
            y = self.remote_height()
            print(f"{self.network} local height:{x} removte height:{y}")
            if x == 0:
                x = self.origin
            if y == 0:
                log.error("get remote block height =0")
                time.sleep(5)
                continue
            if x >= y:
                continue
            for i in range(y - x):
                n = x + i + 1
                head = self.eth.block_head(n)
                self.save_block(head)
                time.sleep(2)
            return
        print("----------END----------")

    def save_block(self, head):
        if head is None:
            return
        print("save block")
        print(head)
        data = {
            "hash": self.eth.to_hex(head.get('hash')),
            "number": head.get('number'),
            "timestamp": head.get('timestamp'),
        }

        self.mongo.insert(self.collection, data)
        self.set_local_height(data['number'], data['timestamp'])

    def set_local_height(self, height, timestamp):
        if height and timestamp:
            self.redis.set(self.tag_height, height)
            self.redis.set(self.tag_timestamp, timestamp)
            print(f"写入redis成功 高度：{height} 时间戳：{timestamp}")

    def local_height(self) -> int:
        h = self.redis.get(self.tag_height)
        if h is None:
            return 0
        else:
            return int(h)

    def remote_height(self) -> int:
        return self.eth.block_height()

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

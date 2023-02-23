# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as log
import time

import utils
from tools.eth_api import EthApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from utils import is_dev_env

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


class Task(object):
    def __init__(self, conf, **kwargs):
        self.network: str = kwargs.get("network")
        self.interval: int = kwargs.get("interval")
        self.origin: int = kwargs.get("origin")
        self.node: str = kwargs.get("node")
        self.webhook: bool = kwargs.get("webhook")

        self.conf: dict = conf
        self.eth: EthApi = self._conn_eth()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()
        self.tag_block = utils.gen_block_tag(network=self.network)
        self.table_name = utils.gen_block_table_name(network=self.network)

    def run(self):
        """
        核心方法，执行引擎
        :return:
        """
        log.info(f"sync block:network:{self.network} origin:{self.origin} webhook:{self.webhook} node:{self.node}")

        while True:
            time.sleep(self.interval)
            x = self._local_height()
            y = self._remote_height()
            log.info(f"{self.network} local height:{x} removte height:{y}")
            if y == 0:
                log.error("get remote block height =0")
                time.sleep(5)
                continue
            if x == 0:
                x = self.origin if self.origin else y - 3
            if x >= y:
                continue
            for i in range(y - x):
                n = x + i + 1
                head = self.eth.block_head(n)
                success = self._save_block(head)
                log.info(
                    f"[progress:{round(100 * (i + 1) / (y - x), 1)}%] sync {self.network} block {n} {'success' if success else 'falied'} ")
                time.sleep(0.5)
        print("----------END----------")

    # 保存block head数据
    def _save_block(self, head) -> bool:
        if head is None:
            return False
        block_height = head.get('number')
        block_timestamp = head.get('timestamp')
        block_hash = self.eth.to_hex(head.get('hash'))

        data = {
            "_id": block_height,
            "hash": block_hash,
            "timestamp": block_timestamp,
        }
        success = self.mongo.insert(self.table_name, data)
        if success:
            self._set_block_cache(height=block_height, timestamp=block_timestamp)
        return success

    # 设置block 同步最新高度缓存，写入redis
    def _set_block_cache(self, height, timestamp):
        if height and timestamp:
            self.redis.setdict(self.tag_block, {'height': height, 'timestamp': timestamp})

    # 获取本地block最新高度缓存，读取redis
    def _local_height(self) -> int:
        b = self.redis.getdict(self.tag_block)
        if not b or not b.get('height'):
            return 0
        else:
            return int(b.get('height'))

    # 获取远程block高度
    def _remote_height(self) -> int:
        return self.eth.block_height()

    # 连接redis
    def _conn_redis(self) -> RedisApi:
        c = self.conf
        if is_dev_env():
            return RedisApi.from_config(**c['redis']['outside'])
        else:
            return RedisApi.from_config(**c['redis']['inside'])

    # 连接mongodb
    def _conn_mongo(self) -> MongoApi:
        c = self.conf
        if is_dev_env():
            return MongoApi.from_conf(**c['mongo']['outside'])
        else:
            return MongoApi.from_conf(**c['mongo']['inside'])

    # 连接以太坊客户端
    def _conn_eth(self) -> EthApi:
        return EthApi.from_node(self.node)

    # # 清除全部数据，mongodb 和redis
    # def _clear_all(self):
    #     log.info("clear all data in mongo ,and clear redis tag")
    #     # 1.清除database
    #     self.mongo.drop(self.table_name)
    #     # 2.清除fredi标识
    #     self.redis.delele(self.tag_height)

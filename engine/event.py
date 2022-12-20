# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 同步 EventOut
# -------------------------------------------------------------------------------
import logging as log
import time
from typing import List

from tools.eth_api import EthApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from uitls import is_dev_env, load_abi

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')

_EvEntName = 'OutEvent'


class Task(object):
    def __init__(self, conf, **kwargs):
        self.conf: dict = conf
        self.network: str = kwargs.get("network").lower()
        self.target: str = kwargs.get("target")
        self.origin: int = kwargs.get("origin")
        self.node: str = kwargs.get("node")
        self.delay: int = kwargs.get('delay')
        self.range: int = kwargs.get('range')
        self.reload: bool = kwargs.get("reload")
        #
        self.eth: EthApi = self._conn_eth()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()
        if not self.eth.is_address(self.target):
            log.error(f"event out target:{self.target} is not a right address ")
            exit()
        self.tag_event = f"event_{self.target[2:6]}_{self.target[-4:]}"
        self.tag_block = f"block_{self.network}_height"
        self.table_name = f"event_{self.target[2:6]}_{self.target[-4:]}"  # evet-77ba-ab12
        self.contract = self._gen_contract()

    def _gen_contract(self):
        abi = load_abi()
        return self.eth.contract_instance(address=self.target, abi=abi)

    def run(self):
        log.info(
            f"sync event:network:{self.network} target:{self.target} origin:{self.origin} reload:{self.reload} node:{self.node}")
        if self.reload:
            self.clear_all()

        while True:
            time.sleep(2)
            x = self.local_height()
            y = self.remote_height()
            # log.info(f"x={x} y={y}")
            if y == 0:
                log.warning("block height is Zero,please check network")
                continue
            if x == 0:
                x = self.origin if self.origin else y - 5

            y = y - self.delay  # 对y进行额外的延时处理,在快速链上，同步慢一个块，防止数据丢失
            if y <= x:
                continue

            a = x
            b = y if (y - x) < self.range else (x + self.range)

            events = self.filte(a, b)
            for i, event in enumerate(events):
                data = {
                    '_id': f"N{event.get('blockNumber')}I{event.get('logIndex')}",
                    'block_number': event.get('blockNumber'),
                    'index': event.get('logIndex'),
                    'tx_hash': self.eth.to_hex(event.get('transactionHash')),
                    'sender': event['args']['sender'],
                    'itype': event['args']['itype'],
                    'bvalue': event['args']['bvalue']
                }
                s = f"save raw event -> sender:{data['sender']} block:{data['block_number']} index:{data['index']} tx_hash:{data['tx_hash']}"
                log.info(s)
                self.mongo.insert(self.table_name, data)
            # 更新tag
            self.redis.set(self.tag_event, b)

    def filte(self, a: int, b: int) -> List[dict]:
        events = self.eth.filte_event(contract=self.contract, event_name=_EvEntName, from_block=a, to_block=b,
                                      arg_filters=None)
        return events

    def local_height(self) -> int:
        h = self.redis.get(self.tag_event)
        if h is None:
            return 0
        else:
            return int(h)

    def remote_height(self) -> int:
        h = self.redis.get(self.tag_block)
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
        self.redis.delele(self.tag_event)

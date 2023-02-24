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

import utils
from tools.eth_api import EthApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from utils import is_dev_env, load_eventout_abi

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
        self.webhook: str = kwargs.get("webhook")

        self.eth: EthApi = self._conn_eth()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()
        if not self.eth.is_address(self.target):
            log.error(f"event out target:{self.target} is not a right address ")
            exit()
        self.table_name = utils.gen_event_table_name(network=self.network, target=self.target)  # event_bsc_77ba-ab12
        self.tag_event = utils.gen_event_tag(network=self.network, target=self.target)
        self.tag_block = utils.gen_block_tag(network=self.network)
        self.contract = self._gen_contract()

    def _gen_contract(self):
        """
        创造智能合约操作对象实体
        :return:
        """
        abi = load_eventout_abi()
        return self.eth.contract_instance(address=self.target, abi=abi)

    def run(self):
        """
        核心方法，启动引擎
        :return:
        """
        log.info(
            f"sync event:network:{self.network} target:{self.target} origin:{self.origin} webhook:{self.webhook} node:{self.node}")
        log.info("good luck")
        while True:
            time.sleep(2)
            x = self._local_event_height()
            y = self._local_block_height()
            log.info(f"local event height={x} local block height={y}")
            if y <= 0:
                log.warning(f"block height is {y},please check network")
                continue
            if x <= 0:
                if self.origin:
                    x = self.origin
                    log.info(f"x =0 event height = origin ={x}")
                else:
                    x = y - 100
                    log.info(f"x=0 event height = (y-100) ={x}")

            y = y - self.delay  # 对y进行额外的延时处理,在快速链上，同步慢一个块，防止数据丢失
            if y <= x:
                continue

            a = x + 1
            b = y if (y - x) <= self.range else (x + self.range)
            log.info(f"filter event in ({a} , {b})")
            events, complete = self._filte(a, b)
            # 1。检测是否访问远程数据成功，如果不成功，跳过本次执行
            if not complete:
                # 如访问区块，过滤日志失败，那么陷入
                time.sleep(1)
                continue
            # 2。遍历events，存入数据库
            for i, event in enumerate(events):
                eid = f"N{event.get('blockNumber')}I{event.get('logIndex')}"
                block_number = event.get('blockNumber')
                index = event.get('logIndex')
                tx_hash = self.eth.to_hex(event.get('transactionHash'))
                sender = event['args']['sender']
                itype = event['args']['itype']
                bvalue = event['args']['bvalue']
                # 根据block高度查询block集合，获取时间戳
                block_timestamp = self._get_block_timestamp(block_number)
                data = {
                    '_id': eid,
                    'block_number': block_number,
                    'block_timestamp': block_timestamp,
                    'index': index,
                    'tx_hash': tx_hash,
                    'sender': sender,
                    'itype': itype,
                    'bvalue': bvalue
                }

                if self.mongo.insert(self.table_name, data):
                    s = f"SUCCESS save event -> sender:{data['sender']} heigh:{data['block_number']} index:{data['index']} tx_hash:{data['tx_hash']} time:{data['block_timestamp']}"
                    log.info(s)
                else:
                    s = f"FAILED save event -> sender:{data['sender']} heigh:{data['block_number']} index:{data['index']} tx_hash:{data['tx_hash']} time:{data['block_timestamp']}"
                    log.error(s)
                # suc = self.mongo.insert(self.table_name, data)
                # if suc:
                #     # 每次插入event数据成功时，更新event local height为N点
                #     cache = {'height': block_number, 'timestamp': block_timestamp}
                #     self.redis.setdict(self.tag_event, cache)
                #     log.info(f"insert success,update event local height -> {cache}")

            # 3。更新本地高度缓存
            t = self._get_block_timestamp(b)
            cache = {'height': b, 'timestamp': t}
            self.redis.setdict(self.tag_event, cache)
            log.info(f"filter complete,update event local height -> {cache}")

    def _filte(self, a: int, b: int) -> (List[dict], bool):
        """
        过滤日志
        :param a: 起始点高度
        :param b: 结束点高度
        :return: event合集，是否完成
        """
        events, complete = self.eth.filte_event(contract=self.contract, event_name=_EvEntName, from_block=a, to_block=b,
                                                arg_filters=None)
        return events, complete

    def _local_event_height(self) -> int:
        """
        获取本地同步高度
        :return: 当前event-out对应的同步高度
        """
        cache = self.redis.getdict(self.tag_event)
        if not cache or not cache.get('height'):
            return 0
        else:
            return cache.get('height')

    def _local_block_height(self) -> int:
        """
        区块高度
        :return: block高度
        """
        block = self.redis.getdict(self.tag_block)
        if not block or not block.get('height'):
            return 0
        else:
            return int(block.get('height'))

    def _conn_redis(self) -> RedisApi:
        """
        连接本地redis数据库
        :return:redis客户端
        """
        c = self.conf
        if is_dev_env():
            return RedisApi.from_config(**c['redis']['outside'])
        else:
            return RedisApi.from_config(**c['redis']['inside'])

    def _conn_mongo(self) -> MongoApi:
        """
        连接本地mongo数据库
        :return: mongo客户端
        """
        c = self.conf
        if is_dev_env():
            return MongoApi.from_conf(**c['mongo']['outside'])
        else:
            return MongoApi.from_conf(**c['mongo']['inside'])

    def _conn_eth(self) -> EthApi:
        """
        连接以太坊客户端
        :return: eth client
        """
        return EthApi.from_node(self.node)

    # def _clear_all(self):
    #     warnings.warn("this method is not support by engine")
    #     log.info("clear all data in mongo ,and clear redis tag")
    #     # 1.清除database
    #     self.mongo.drop(self.table_name)
    #     # 2.清除fredi标识
    #     self.redis.delele(self.tag_event)

    def _get_block_timestamp(self, h: int) -> int:
        """
        获取block高度对应的时间戳
        :param h:
        :return:
        """
        block_coll = utils.gen_block_table_name(network=self.network)
        block = self.mongo.find_one(c=block_coll, filte={'_id': h})
        if block:
            return block.get('timestamp')
        else:
            head = self.eth.block_head(h)
            log.warning("can not find block in database,so to net")
            if head:
                return head.get('timestamp')
            else:
                return int(time.time())

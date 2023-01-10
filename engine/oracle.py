# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from dataclasses import dataclass

from tools.eth_api import EthApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from utils import is_dev_env


#   string netwrok = 1;// 区块网络,eg:bsc
#   string provider = 2;//供应商eg:chainlink,uniswapv2
#   string target = 3;// 喂价源地址
#   uint64 history = 4;// 历史数据，默认为0，即当前时刻开始同步。
#   string node = 5; // 访问节点，必须有
#   string webhook = 6;// 飞书信息钩子地址，error或者info级别的日志将回调发射到本地中，默认空

@dataclass
class Demo:
    Name: str
    Country: str
    Age: int
    pass


class Task(object):
    def __init__(self, conf, **kwargs):
        self.conf = conf
        self.netwrok = kwargs.get('netwrok')
        self.provider = kwargs.get('provider')
        self.target = kwargs.get('target')
        self.history = kwargs.get('history')
        self.node = kwargs.get('node')
        self.webhook = kwargs.get('webhook')

    def run(self):
        # TODO 实现oracle同步引擎
        print(f"network:{self.netwrok}")
        print("TODO:还没写")

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

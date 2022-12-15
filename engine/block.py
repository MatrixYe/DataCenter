# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import argparse
import time
from typing import Union
import logging as log

import web3
from web3 import Web3
from tools.redis_api import RedisApi
from tools.eth_api import EthApi
from tools.mongo_api import MongoApi
from tools.uitls import is_dev_env, load_config

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


class Task(object):
    def __init__(self, **kwargs):
        self.network: str = kwargs.get("network")
        self.interval: int = kwargs.get("interval")
        self.origin: int = kwargs.get("origin")
        self.node: str = kwargs.get("node")
        self.reload: bool = kwargs.get("reload")
        #
        self.conf: dict = load_config()
        self.eth: EthApi = self._conn_eth()
        self.rs: RedisApi = self._conn_redis()
        self.mongo = self._conn_mongo()

    def run(self):
        ok, err = self._check()
        if not ok:
            log.error(f"check error:{err}")
            return
        # log.debug(f"sync block:network:{self.network} origin:{self.origin} reload:{self.reload} node:{self.node}")

    def _check(self) -> (bool, Union[str, None]):
        if not self.network:
            return False, "network is None!"
        if not self.node:
            return False, 'node node in None!'
        if self.reload is None:
            return False, 'reload can not be none,must be True or False'
        if self.origin <= 0:
            return False, 'block origin must > 0'
        if self.interval <= 0:
            return False, 'interval must > 0'
        return True, None

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

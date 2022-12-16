# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from typing import Union
import logging as log
from web3.middleware import geth_poa_middleware
from web3 import Web3, HTTPProvider

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


# noinspection PyBroadException
class EthApi(object):
    def __init__(self, endpoint_uri=None, request_kwargs=None, session=None):
        if not endpoint_uri:
            raise "can not init eth client,endpoint_uri is None"
        self.client = Web3(HTTPProvider(endpoint_uri=endpoint_uri, request_kwargs=request_kwargs, session=session))
        self.client.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件

    @classmethod
    def from_node(cls, node: str):
        parmas = dict()
        parmas['endpoint_uri'] = node
        parmas['request_kwargs'] = None
        parmas['session'] = None
        return cls(**parmas)

    # 获取当前最新区块高度
    def block_height(self) -> Union[int]:
        try:
            return self.client.eth.block_number
        except Exception as e:
            log.error(e)
            return 0

    # 获取区块头信息
    def block_head(self, height: int):
        try:
            return self.client.eth.get_block(height)
        except Exception as e:
            log.error(e)
            return None

    # 判断是否是正确的地址
    def is_address(self, addr) -> bool:
        return self.client.isAddress(addr)

    def to_text(self, v) -> str:
        return self.client.toText(v)

    def to_hex(self, v) -> str:
        return self.client.toHex(v)

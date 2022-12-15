# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import web3
from typing import Union


# noinspection PyBroadException
class EthApi(object):
    def __init__(self, endpoint_uri=None, request_kwargs=None, session=None):
        if not endpoint_uri:
            raise "can not init eth client,endpoint_uri is None"
        self.client = web3.Web3(
            web3.HTTPProvider(endpoint_uri=endpoint_uri, request_kwargs=request_kwargs, session=session))

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
            return 0

    # 获取区块头信息
    def block_head(self, height: int):
        try:
            return self.client.eth.get_block(height)
        except Exception as e:
            return None

    # 判断是否是正确的地址
    def is_address(self, addr) -> bool:
        return self.client.isAddress(addr)

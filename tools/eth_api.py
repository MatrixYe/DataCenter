# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as log
from typing import List
from typing import Union

from web3 import Web3, HTTPProvider
from web3.eth import LogReceipt, Contract, ChecksumAddress
from web3.middleware import geth_poa_middleware

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


# noinspection PyBroadException
class EthApi(object):
    def __init__(self, endpoint_uri=None, request_kwargs=None, session=None):
        if not endpoint_uri:
            raise "can not init eth client,endpoint_uri is None"
        self.client: Web3 = Web3(
            HTTPProvider(endpoint_uri=endpoint_uri, request_kwargs=request_kwargs, session=session))
        self.client.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件,兼容BSc、RInkeby等区块链网络

    def is_connected(self):
        return self.client.isConnected()

    @classmethod
    def from_node(cls, node: str):
        if not node:
            raise Exception('creart eth client failed:node is empty')
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

    # 转化成16进制字符串
    def to_hex(self, v) -> str:
        return self.client.toHex(v)

    # 将地址字符串、字节数组转化成Address结构体
    def check_sum_address(self, address: Union[str, bytes]) -> ChecksumAddress:
        return self.client.toChecksumAddress(address)

    # 构造合约实例对象
    def contract_instance(self, address: str, abi) -> Union[Contract, None]:
        try:
            addr = self.client.toChecksumAddress(address)
            c = self.client.eth.contract(address=addr, abi=abi)
            return c
        except BaseException as e:
            log.error(f'can not gen contract instance,check address or abi file:{e}')
            return None

    @staticmethod
    def filte_event(contract: Contract, event_name: str, from_block: int, to_block: int, arg_filters: dict = None) -> \
            List[LogReceipt]:
        """

        :param contract: 合约实例
        :param event_name: 事件名称
        :param from_block: 开始区块高度
        :param to_block: 结束区块高度
        :param arg_filters: 参数过滤，eg: {'itype':2}
        :return:
        """
        # https://web3py.readthedocs.io/en/v5/contracts.html#web3.contract.Contract.events.your_event_name.createFilter
        f = contract.events[event_name].createFilter(fromBlock=from_block, toBlock=to_block,
                                                     argument_filters=arg_filters)
        return f.get_all_entries()

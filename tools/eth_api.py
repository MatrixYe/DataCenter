# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 以太坊链相关Api工具
# -------------------------------------------------------------------------------
import logging as log
from typing import List
from typing import Union

from web3 import Web3, HTTPProvider
from web3.eth import LogReceipt, Contract, ChecksumAddress
from web3.middleware import geth_poa_middleware
from web3.middleware import simple_cache_middleware

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


# noinspection PyBroadException
class EthApi(object):
    def __init__(self, endpoint_uri=None, request_kwargs=None, session=None):
        if not endpoint_uri:
            raise "can not init eth client,endpoint_uri is None"
        self.client: Web3 = Web3(
            HTTPProvider(endpoint_uri=endpoint_uri, request_kwargs=request_kwargs, session=session))
        #  注入poa中间件,兼容BSc、RInkeby等区块链网络
        self.client.middleware_onion.inject(geth_poa_middleware, layer=0)  #
        # 此属性在验证中间件中频繁调用， 但默认情况下chain_id会添加到 中。 将simple_cache_middleware添加到 以提高性能：simple_cache_middlewaremiddleware_onion
        self.client.middleware_onion.add(simple_cache_middleware)

    def is_connected(self) -> bool:
        """
        是否连接
        :return:
        """
        return self.client.isConnected()

    def chain_id(self) -> int:
        """
        返回链标识 chain-id
        :return:
        """
        return self.client.eth.chain_id

    def chain_name(self):
        # self.client.eth
        pass

    @classmethod
    def from_node(cls, node: str):
        """
        通过节点构建eth客户端
        :param node:
        :return:
        """
        if not node:
            raise Exception('creart eth client failed:node is empty')
        parmas = dict()
        parmas['endpoint_uri'] = node
        parmas['request_kwargs'] = None
        parmas['session'] = None
        return cls(**parmas)

    def block_height(self) -> Union[int]:
        """
        获取当前最新区块高度
        :return:
        """
        try:
            return self.client.eth.block_number
        except Exception as e:
            log.error(e)
            return 0

    def block_head(self, height: int):
        """
        获取区块头信息
        :param height:
        :return:
        """
        try:
            return self.client.eth.get_block(height)
        except Exception as e:
            log.error(e)
            return None

    def is_address(self, addr) -> bool:
        """
        判断是否是正确的地址
        :param addr:
        :return:
        """
        return self.client.isAddress(addr)

    def to_text(self, v) -> str:
        """
        获取客户端名称
        :param v:
        :return:
        """
        return self.client.toText(v)

    def to_hex(self, v) -> str:
        """
        转化成16进制字符串

        :param v:
        :return:
        """
        try:
            return self.client.toHex(v)
        except Exception as e:
            log.error(f"to hex error:{e}")
            return '0xUNKNOWN'

    def check_sum_address(self, address: Union[str, bytes]) -> ChecksumAddress:
        """
        将地址字符串、字节数组转化成Address结构体
        :param address:
        :return:
        """
        return self.client.toChecksumAddress(address)

    def contract_instance(self, address: str, abi) -> Union[Contract, None]:
        """
        构造合约实例对象
        :param address:
        :param abi:
        :return:
        """
        try:
            addr = self.client.toChecksumAddress(address)
            c = self.client.eth.contract(address=addr, abi=abi)
            return c
        except BaseException as e:
            log.error(f'can not gen contract instance,check address or abi file:{e}')
            return None

    @staticmethod
    def filte_event(contract: Contract, event_name: str, from_block: int, to_block: int, arg_filters: dict = None) -> \
            (List[LogReceipt], bool):
        """

        :param contract: 合约实例
        :param event_name: 事件名称
        :param from_block: 开始区块高度
        :param to_block: 结束区块高度
        :param arg_filters: 参数过滤，eg: {'itype':2}
        :return:List[LogReceipt]
        """
        # https://web3py.readthedocs.io/en/v5/contracts.html#web3.contract.Contract.events.your_event_name.createFilter
        try:
            f = contract.events[event_name].createFilter(fromBlock=from_block,
                                                         toBlock=to_block,
                                                         argument_filters=arg_filters)
            return f.get_all_entries(), True
        except Exception as e:
            log.error(
                f"filter event failed: name={event_name} from = {from_block} to={to_block} arg={arg_filters}-> {e}")
            return [], False

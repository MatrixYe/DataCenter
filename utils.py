# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import json
import platform
import time
from typing import Union

import toml

# 以太坊系列 区块网络名称及chain-id
with open('networks.toml', 'r') as f:
    _networks = toml.load(f, _dict=dict)
    # _networks = json.load(f)

with open('config.toml', 'r') as f:
    _config = toml.load(f, _dict=dict)


def load_config(file_path=None) -> dict:
    """
    加载默认配置
    :param file_path:
    :return:
    """
    return _config


def load_redis_config() -> dict:
    """
    加载redis配置
    :return:
    """
    c = load_config()
    return c['redis']


def load_docker_net() -> dict:
    """
    加载docker 默认局域网名称
    :return:
    """
    c = load_config()
    return c['network']


def is_dev_env() -> bool:
    """
    是否在宿主上运行
    :return: bool True：主机上，False:docker 容器中
    """
    return platform.system() in ("Windows", "Darwin")


def load_eventout_abi(file_path: str = None) -> Union[dict, None]:
    """
    加载 event out abi
    :param file_path:
    :return:
    """
    if file_path is None:
        file_path = './source/EventOut.json'
    with open(file_path, 'r') as fs:
        return json.load(fs)


def is_address(addr: str) -> bool:
    """
    判断是否正确地址
    :param addr: 地址
    :return: True 正确地址，False非法地址
    """
    if not addr:
        return False
    if not addr.startswith('0x'):
        return False
    if len(addr) < 32:
        return False

    return True


def gen_docker_net_alias(contailer_name: str) -> str:
    """
    获取docker 局域网 容器ip别名
    :param contailer_name: 容器名
    :return:
    """
    return f"{contailer_name}host"


def gen_block_continal_name(network: str) -> str:
    """
    # 生成sync block同步容器名称

    :param network: 区块网络
    :return: 容器名称
    """
    return f"block-{network}"


def gen_event_container_name(network: str, target: str) -> str:
    """
    生成sync event 同步容器名称

    :param network: 区块网络
    :param target: event out 地址
    :return: event sync 容器名称
    """
    return f"event-{network}-{target[2:6]}-{target[-4:]}"


def gen_oracle_container_name(network: str, provider: str, target: str) -> str:
    """
    # 生成sync oracle 同步容器名称

    :param network: 区块网络
    :param provider: 喂价源供应商，例如chainlink、uniswapv2 、uniswapv3 ...
    :param target: 喂价源地址
    :return: oracle 容器名称
    """
    return f"oracle-{network}-{provider}-{target[2:6]}-{target[-4:]}"


def gen_block_table_name(network: str) -> str:
    """
    生成block同步数据的表，即mongodb中的collection

    :param network: 区块网络
    :return: 表的名称 eg: block_bsc
    """
    return f"block_{network}"


def gen_block_tag(network: str):
    return f"block_{network}"


def gen_event_table_name(network: str, target: str) -> str:
    """
    生成event out 数据 表名

    :param network: 区块网络
    :param target: event out地址
    :return: 表名
    """
    target = target.lower()
    return f"event_{network}_{target[2:6]}_{target[-4:]}"


def gen_event_tag(network: str, target: str) -> str:
    """
    生成 event out 在redis中的记录缓存
    :param network: 区块网络
    :param target: event out地址
    :return: event的redis缓存key
    """
    target = target.lower()
    return f"event_{network}_{target[2:6]}_{target[-4:]}"


def check_network(network: str) -> bool:
    """
    检测 network是否合法

    :param network:
    :return: bool：是否合法的network名称
    """
    if not network:
        return False

    if network.lower() not in _networks.keys():
        return False
    return True


def get_chain_id(network: str) -> int:
    """
    获取network对应的chainID
    :param network: 区块网络名称
    :return: chain id
    """
    if not network:
        return 0
    cid = _networks.get(network.lower())
    if not cid:
        return 0
    return cid


def get_network_and_cid(network: Union[str, None], chain_id: Union[int, None]) -> (Union[str, None], Union[int, None]):
    """
    通过输入的network和chainid 返回合法的network和chainid
    :param network: 输入的network
    :param chain_id: 输入的chainid
    :return: 返回符合配置文件的network和chainid
    """
    if not network and not chain_id:
        return None, None
    # 优先chain id判断
    if chain_id:
        for k, v in _networks.items():
            if v == chain_id:
                return k, v
    elif network:
        v = _networks.get(network)
        if v:
            return network, v
    return None, None


# def get_network_byid
def get_network_name(chain_id: Union[int, None]) -> Union[str, None]:
    """
    通过chainid获取区块链网络名称
    :rtype: object
    :param chain_id:
    :return: 
    """
    for k, v in _networks.items():
        if v == chain_id:
            return k


def support_network() -> Union[dict, None]:
    return _networks


def now(t=None, fm="%Y-%m-%d %H:%M:%S") -> str:
    return time.strftime(fm, time.localtime(t))

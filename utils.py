# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import json
import platform
from typing import Union


def load_config(file_path=None) -> dict:
    """
    加载默认配置
    :param file_path:
    :return:
    """
    if file_path is None:
        file_path = "config.json"
    with open(file_path, 'r') as f:
        return json.load(f)


def load_redis_config() -> dict:
    """
    加载redis配置
    :return:
    """
    c = load_config()
    return c['redis']


def load_pg_config() -> dict:
    """
    加载postgres配置
    :return:
    """
    c = load_config()
    return c['postgres']


def load_docker_net():
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
    with open(file_path, 'r') as f:
        return json.load(f)


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
    :return: 表的名称
    """
    return f"block_{network}"


def gen_block_cache_name(network: str) -> str:
    """
    生成block同步数据高度缓存 redis key
    :param network:
    :return:
    """
    return f"block_{network}_height"


def gen_event_table_name(network: str, target: str) -> str:
    """
    生成event out 数据 表名

    :param network: 区块网络
    :param target: event out地址
    :return: 表名
    """
    return f"event_{network}_{target[2:6]}_{target[-4:]}"


def gen_event_cache_name(network: str, target: str) -> str:
    """
    生成 event out 在redis中的记录缓存
    :param network: 区块网络
    :param target: event out地址
    :return:
    """
    return f"event_{network}_{target[2:6]}_{target[-4:]}"

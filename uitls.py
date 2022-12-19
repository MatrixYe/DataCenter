# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import platform
import json
from typing import Union


def load_config(file_path=None) -> dict:
    if file_path is None:
        file_path = "config.json"
    with open(file_path, 'r') as f:
        return json.load(f)


def load_redis_config() -> dict:
    c = load_config()
    return c['redis']


def load_pg_config() -> dict:
    c = load_config()
    return c['postgres']


def load_docker_net():
    c = load_config()
    return c['network']


def is_dev_env() -> bool:
    """
    是否在宿主上运行
    :return: bool True：主机上，False:docker 容器中
    """
    return platform.system() in ("Windows", "Darwin")


def load_abi(file_path: str = None) -> Union[dict, None]:
    if file_path is None:
        file_path = './source/EventOut.json'
    with open(file_path, 'r') as f:
        return json.load(f)

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from typing import Union

from fastapi import APIRouter

import utils
from tools.control import BlockCtrl, EventCtrl
from tools.docker_api import DockerApi
from .basic import Reply

router = APIRouter()
docker = DockerApi.from_env()
block_ctrl = BlockCtrl(utils.load_config())
event_ctrl = EventCtrl(utils.load_config())


### 获取支持的区块网络


@router.get("/networks")
async def networks(search: Union[str, int, None] = None):
    values = utils.support_network()
    # if search:
    #     ks = values.keys()
    #     pass
    return Reply.com(values)


@router.get("/network")
async def network_info(name: str = None, chain_id: int = None):
    if name:
        _id = utils.get_chain_id(name)
        return Reply.com(_id, f"unknown network {name}")
    elif chain_id:
        name = utils.get_network_name(chain_id)
        return Reply.com(name, f"unkonw chain_id {chain_id}")
    else:
        return Reply.err("unknow network name or chain id")


@router.get("/tasks")
async def tasks():
    block_info = block_ctrl.task_info()
    event_info = event_ctrl.task_info()
    return Reply.com({'block_task': block_info, 'event_task': event_info}, 'unknown error')

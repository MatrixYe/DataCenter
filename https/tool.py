# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from fastapi import APIRouter

# from utils import support_network, get_chain_id
import utils
from .basic import Reply

router = APIRouter()


### 获取支持的区块网络


@router.get("/networks")
async def networks():
    values = utils.support_network()
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

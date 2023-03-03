# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------


from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel

import utils
from tools.eth_api import EthApi
from .basic import Reply

router = APIRouter()


class AskStartBlock(BaseModel):
    #   string network = 1;//区块网络
    #   uint64 origin = 2;// 区块高度起始点
    #   uint32 interval = 3;// 区块扫描周期，单位秒
    #   string node = 4;// 请求体节点
    #   string webhook = 5;// 飞书信息钩子，error或者info级别的日志将回调发射到本地中，默认空
    chain_id: int
    node: str
    interval: float = 10
    webhook: Union[str, None] = None


@router.post(path="/start")
async def start_sync_block(ask: AskStartBlock):
    """
        启动一条新的block链同步的
    :return:
    """
    if not ask.node:
        return Reply.err("node is empty")
    if ask.chain_id == 4:
        return Reply.err("rinkeby(chain_id=4) is abandoned network,forbid sync this blockchain")
    network = utils.get_network_name(ask.chain_id)
    if not network:
        return Reply.err(
            f"unsupport chain_id ,can not find network by chainid:{ask.chain_id},please update 'networks.json'")
    eth: EthApi = EthApi.from_node(ask.node)
    if not eth.is_connected():
        return Reply.err("node is not connect,check it")
    cid = eth.chain_id()
    if cid != ask.chain_id:
        return Reply.err(f"ask chain_id is {ask.chain_id},but node chain_id is {cid}")
    coll = utils.gen_block_table_name(network)
    container = utils.gen_block_continal_name(network)
    tag = utils.gen_block_tag(network)
    return Reply.suc(
        {
            "chain_id": ask.chain_id,
            "node": ask.node,
            "interval": ask.interval,
            "webhook": ask.webhook,
            "network": network,
            'coll': coll,
            "container": container,
            "tag": tag
        }
    )


@router.post(path="/stop")
async def stop_sync_block():
    """

    :return:
    """
    return "TODO"


@router.post(path="/restart")
async def restart_sync_block():
    """

    :return:
    """
    return "TODO"


@router.post(path="/last")
async def last_block():
    """

    :return:
    """
    return "TODO"

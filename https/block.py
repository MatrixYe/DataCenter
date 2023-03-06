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
from tools.control import BlockCtrl
from tools.eth_api import EthApi
from .basic import Reply

IMG_SYNC_EVENT = "sync-event:latest"
IMG_SYNC_BLOCK = "sync-block:latest"
IMG_SYNC_ORACLE = "sync-oracle:latest"

router = APIRouter()
block_ctrl = BlockCtrl(utils.load_config())


class AskStartBlock(BaseModel):
    network: Union[str, None] = None
    chain_id: Union[int, None] = None
    node: str
    interval: int = 10
    webhook: Union[str, None] = 'None'
    check_node: bool = True


class AskRemoveBlock(BaseModel):
    network: Union[str, None] = None
    chain_id: Union[int, None] = None
    delete: bool = False


@router.post(path="/start")
async def start_sync_block(ask: AskStartBlock):
    """
        启动一条新的block链同步的
    :return:
    """
    if not ask.node:
        return Reply.err("can not sync block,node is empty")
    if ask.chain_id == 4:
        return Reply.err("rinkeby(chain_id=4) is abandoned network,forbid sync this blockchain")

    _network = utils.get_network_name(ask.chain_id) if ask.chain_id else ask.network
    _cid = ask.chain_id if ask.chain_id else utils.get_chain_id(_network)

    if not _network or not _cid:
        return Reply.err(
            f"can not sync,unsupport chain_id={_cid} or network={_network},please update 'networks.json'")

    if ask.check_node:
        eth: EthApi = EthApi.from_node(ask.node)
        if not eth.is_connected():
            return Reply.err("can not sync block,node is not connect,check it", 1002)
        cid = eth.chain_id()
        if cid != _cid:
            return Reply.err(f"can not sync block,ask chain_id is {_cid},but node chain_id is {cid}")

    coll = utils.gen_block_table_name(_network)
    tag = utils.gen_block_tag(_network)
    cn, ac = block_ctrl.start_block(network=_network, origin=0, interval=ask.interval, node=ask.node,
                                    webhook=ask.webhook)

    if 'failed' in ac or cn is None:
        return Reply.err("start container failed!!")
    if 'pass' in ac:
        return Reply.err(f'container {cn.name} is exist,can not submit task,please remove or restart')
    return Reply.suc(
        {
            "network": _network,
            'mongo': coll,
            "container": {"name": cn.name, "status": cn.status, "short_id": cn.short_id},
            "redis": tag,
            "action": ac
        }
    )


@router.post(path="/restart")
async def restart_sync_block(ask: AskStartBlock):
    """

    :return:
    """
    if not ask.node:
        return Reply.err("can not sync block,node is empty")
    if ask.chain_id == 4:
        return Reply.err("rinkeby(chain_id=4) is abandoned network,forbid sync this blockchain")

    _network = utils.get_network_name(ask.chain_id) if ask.chain_id else ask.network
    _cid = ask.chain_id if ask.chain_id else utils.get_chain_id(_network)

    if not _network or not _cid:
        return Reply.err(f"can not sync,unsupport chain_id={_cid} or network={_network},update 'networks.json'")

    if ask.check_node:
        eth: EthApi = EthApi.from_node(ask.node)
        if not eth.is_connected():
            return Reply.err("can not sync block,node is not connect,check it", 1002)
        cid = eth.chain_id()
        if cid != _cid:
            return Reply.err(f"can not sync block,ask chain_id is {_cid},but node chain_id is {cid}")

    coll = utils.gen_block_table_name(_network)
    tag = utils.gen_block_tag(_network)
    cn, ac = block_ctrl.start_block(network=_network, origin=0, interval=ask.interval, node=ask.node,
                                    webhook=ask.webhook, restart=True)
    if 'failed' in ac or cn is None:
        return Reply.err("start container failed!!")
    if 'pass' in ac:
        return Reply.err(f'container {cn.name} is a exist,can not submit task,please remove or restart')
    return Reply.suc(
        {
            "network": _network,
            'mongo': coll,
            "container": {"name": cn.name, "status": cn.status, "short_id": cn.short_id},
            "redis": tag,
            "action": ac
        }
    )


@router.post(path="/remove")
async def remove_sync_block(ask: AskRemoveBlock):
    """

    :return:
    """
    network = ask.network
    cid = ask.chain_id
    delete = ask.delete

    _network = utils.get_network_name(cid) if cid else network
    if not _network:
        return Reply.err(f"can not remove {_network}-block,network or cid is None")

    cname, msg = block_ctrl.remove_block(network=_network, delete=delete)
    if 'remove' not in msg:
        return Reply.err(f'can not remove {cname},container is not exist')
    return Reply.suc(data={"network": _network, "container": cname, "removedb": delete, "result": msg})


@router.get(path="/last")
async def last_block(network: Union[str, None] = None, chain_id: Union[int, None] = None):
    network_ = utils.get_network_name(chain_id) if chain_id else network
    last = block_ctrl.last_block(network_)
    return Reply.com(last, f'can not fint last block by network {network_}')

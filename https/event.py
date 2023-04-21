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
from tools.control import EventCtrl
from tools.eth_api import EthApi
from .basic import Reply

router = APIRouter()
event_ctrl = EventCtrl(utils.load_config())


class AskStartEvent(BaseModel):
    network: Union[str, None]
    chain_id: Union[int, None]
    target: str
    origin: int
    node: str
    delay: int = 10
    range: int = 2000
    webhook: Union[str, None] = 'None'
    check_node: bool = True


class AskRestartEvent(BaseModel):
    network: Union[str, None]
    chain_id: Union[int, None]
    target: str
    origin: int
    node: str
    delay: int = 10
    range: int = 2000
    webhook: Union[str, None] = 'None'
    check_node: bool = True
    clear: bool = False


class AskRemoveEvent(BaseModel):
    network: Union[str, None]
    chain_id: Union[int, None]
    target: str
    clear: bool = False


@router.post(path="/start")
async def start_sync_event(ask: AskStartEvent):
    _network, _cid = utils.get_network_and_cid(network=ask.network, chain_id=ask.chain_id)
    if not _network or not _cid:
        Reply.err(f'network {ask.network} not match chainid {ask.chain_id},please input a right network or chainid')
    if not utils.is_address(ask.target):
        return Reply.err(f"fcan not sync event,illegal target {ask.target}")
    if ask.origin <= 0 or ask.delay < 0 or ask.delay > 10 or ask.range < 0:
        return Reply.err(f"can not sync event,illegal origin {ask.origin}、delay {ask.delay}、range {ask.range}")

    if ask.check_node:
        eth: EthApi = EthApi.from_node(ask.node)
        if not eth.is_connected():
            return Reply.err("can not sync event,node is not connect,check it", 1002)
        cid = eth.chain_id()
        if cid != _cid:
            return Reply.err(f"can not sync event,ask chain_id is {_cid},but node chain_id is {cid}")

    cn, ac = event_ctrl.start_event(_network, ask.target, ask.origin, ask.node, ask.delay, ask.range, ask.webhook)
    if 'failed' in ac or cn is None:
        return Reply.err("start container failed!!")
    if 'pass' in ac:
        return Reply.err(f'container {cn.name} is exist,can not submit task,please remove or restart')
    coll = utils.gen_event_table_name(_network, ask.target)
    tag = utils.gen_event_tag(_network, ask.target)

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
async def restart_sync_event(ask: AskRestartEvent):
    _network, _cid = utils.get_network_and_cid(network=ask.network, chain_id=ask.chain_id)
    if not _network or not _cid:
        Reply.err(f'network {ask.network} not match chainid {ask.chain_id},please input a right network or chainid')

    if not _network:
        return Reply.err(f"can not sync event,illegal network {_network}")
    if not utils.is_address(ask.target):
        return Reply.err(f"fcan not sync event,illegal target {ask.target}")
    if ask.origin <= 0 or ask.delay < 0 or ask.delay > 10 or ask.range < 0:
        return Reply.err(f"can not sync event,illegal origin {ask.origin}、delay {ask.delay}、range {ask.range}")

    if ask.check_node:
        eth: EthApi = EthApi.from_node(ask.node)
        if not eth.is_connected():
            return Reply.err("can not sync block,node is not connect,check it", 1002)
        cid = eth.chain_id()
        if cid != _cid:
            return Reply.err(f"can not sync block,ask chain_id is {_cid},but node chain_id is {cid}")

    cn, ac = event_ctrl.restart_event(_network, ask.target, ask.origin, ask.node, ask.delay, ask.range, ask.webhook,
                                      ask.clear)
    if 'failed' in ac or cn is None:
        return Reply.err("start container failed!!")
    if 'pass' in ac:
        return Reply.err(f'container {cn.name} is exist,can not submit task,please remove or restart')
    coll = utils.gen_event_table_name(_network, ask.target)
    tag = utils.gen_event_tag(_network, ask.target)

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
async def remove_sync_event(ask: AskRemoveEvent):
    _network, _cid = utils.get_network_and_cid(network=ask.network, chain_id=ask.chain_id)
    if not _network or not _cid:
        Reply.err(f'can not parse network {ask.network} or chainid {ask.chain_id},check it or update config')
    cn, ac = event_ctrl.remove_event(_network, ask.target, ask.clear)
    if 'remove' not in ac:
        return Reply.err(f'can not remove {cn},container is not exist')
    return Reply.suc(data={"network": _network, "container": cn, "clear": ask.clear, "result": ac})


@router.get(path="/last")
async def last_event(target: str, network: Union[str, None] = None, chain_id: Union[int, None] = None):
    _network, _cid = utils.get_network_and_cid(network=network, chain_id=chain_id)
    if not _network or not _cid:
        Reply.err(f'can not parse network {network} or chainid {chain_id},check it or update config')
    last = event_ctrl.last_event(_network, target)
    return Reply.com(last, f'can not fint last event by network={_network} target={target}')


@router.post(path="/filter")
async def filter_():
    return "todo"
    pass

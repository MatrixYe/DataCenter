# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------


from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class StartBlockReq(BaseModel):
    #   string network = 1;//区块网络
    #   uint64 origin = 2;// 区块高度起始点
    #   uint32 interval = 3;// 区块扫描周期，单位秒
    #   string node = 4;// 请求体节点
    #   string webhook = 5;// 飞书信息钩子，error或者info级别的日志将回调发射到本地中，默认空
    chain_id: int

    pass


@router.post(path="/start")
async def start_sync_block():
    """
        启动一条新的block链同步的
    :return:
    """
    return "TODO"


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


@router.post(path="/detail")
async def detail_block():
    """

    :return:
    """
    return "TODO"

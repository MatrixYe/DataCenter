# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from fastapi import APIRouter

router = APIRouter()


@router.post(path="/start")
async def start_sync_event():
    pass

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import time

from tools import docker_api
import pprint
from . import ctrl

pp = pprint.PrettyPrinter(indent=2)


def start(host: str, port: int, **kwargs):
    print(f"host={host} port={port}")
    infos = docker_api.info()
    pp.pprint(infos)
    # --network
    # bsc
    # --origin
    # 23836740
    # --interval
    # 2
    # --node
    # https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/
    # --reload
    # False

    print("测试重新开始同步bsc")
    ctrl.sync_block(network='bsc', origin=0, interval=2,
                    node='https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/',
                    reload=False)
    time.sleep(100)

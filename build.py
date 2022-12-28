# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import os

engines = [
    {
        'name': 'Block Engine',
        'cmd': 'docker build -t sync-block . -f imager/sync_block.Dockerfile',
        'desc': '构建区块高度同步器基础镜像'
    }, {
        'name': 'Event Engine',
        'cmd': 'docker build -t sync-event . -f imager/sync_event.Dockerfile',
        'desc': '构建通用事件同步器基础镜像'
    },
    {
        'name': 'Oracle Engine',
        'cmd': 'docker build -t sync-oracle . -f imager/sync_oracle.Dockerfile',
        'desc': '构建喂价源同步器基础镜像'
    },
    {
        'name': 'Rpc Server',
        'cmd': 'docker build -t server . -f imager/server.Dockerfile',
        'desc': '构建RPC服务镜像'
    }
]
if __name__ == '__main__':
    print("-------- START --------")
    for i, e in enumerate(engines):
        print(f"{i + 1}: {e['name']} {e['desc']}")
    i = int(input("Pleace chose image of engine:  "))
    if i < 0:
        exit()
    if i == 0:
        for i, engine in enumerate(engines):
            print(engine['cmd'])
            os.system(engine['cmd'])
    else:
        cmd = engines[i - 1]['cmd']
        print(cmd)
        os.system(cmd)

    print("--------- END ---------")

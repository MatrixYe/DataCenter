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
        'desc': 'block data sync engine'
    }, {
        'name': 'Event Engine',
        'cmd': 'docker build -t sync-event . -f imager/sync_event.Dockerfile',
        'desc': 'event out data sync engine'
    },
    {
        'name': 'Oracle Engine',
        'cmd': 'docker build -t sync-oracle . -f imager/sync_oracle.Dockerfile',
        'desc': 'oracle price data sync engine'
    }
]
if __name__ == '__main__':
    print("-------- START --------")
    for i, e in enumerate(engines):
        print(f"{i + 1}: {e['name']} {e['desc']}")
    i = int(input("Pleace chose image of engine:  "))
    cmd = engines[i - 1]['cmd']
    print(cmd)
    os.system(cmd)
    print("--------- END ---------")

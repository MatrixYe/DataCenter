# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from engine.block import Task
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
# 区块网络
parser.add_argument("--network", type=str)
# 起始点
parser.add_argument("--origin", type=int)
# 扫描周期
parser.add_argument("--interval", type=int)
# 连接节点
parser.add_argument("--node", type=str)
# 重新同步
parser.add_argument("--reload", type=lambda x: (str(x).lower() in ('true', '1', 't')), default=False)

args = parser.parse_args()

if __name__ == '__main__':
    task = Task(network=args.network, origin=args.origin, interval=args.interval, node=args.node, reload=args.reload)
    task.run()

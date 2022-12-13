# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from engine.event import Task
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
# 区块网络
parser.add_argument("--network", type=str)
# 目标eventout地址
parser.add_argument("--target", type=str)
# 同步起始点
parser.add_argument("--origin", type=int)
# 连接节点
parser.add_argument("--node", type=str)
# 是否重新同步(谨慎)
parser.add_argument("--reload", type=bool)

args = parser.parse_args()

if __name__ == '__main__':
    task = Task(network=args.network, target=args.target, origin=args.origin, node=args.node, reload=args.reload)
    task.run()

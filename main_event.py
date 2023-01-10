# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import argparse
import logging as log
import platform

from engine.event import Task
from utils import load_config

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
# 1区块网络
parser.add_argument("--network", type=str)
# 2目标eventout地址
parser.add_argument("--target", type=str)
# 3同步起始点
parser.add_argument("--origin", type=int)
# 4连接节点
parser.add_argument("--node", type=str)
# 5延时同步，针对比较快的链
parser.add_argument("--delay", type=int, default=0)
# 6 一次性最大同步的区块跨度
parser.add_argument("--range", type=int, default=1000)
# 7 是否重新同步(谨慎为True)
parser.add_argument("--reload", type=lambda x: (str(x).lower() in ('true', '1', 't')), default=False)

args = parser.parse_args()


def check_args():
    if not args.network:
        log.error("network is None!")
        exit()
    if not args.target:
        log.error("target is None!")
        exit()
    if args.origin < 0:
        log.error('block origin must > 0')
        exit()
    if not args.node:
        log.error('node node in None!')
        exit()
    if args.reload is None:
        log.error('reload can not be none,must be True or False')
        exit()
    if args.range < 100 or args.range > 10000:
        log.error("range must >100 and must <1w")
        exit()
    if args.delay > 5 or args.delay < 0:
        log.error("delay must <5 and >0")
        pass


if __name__ == '__main__':
    log.info(f"Args Input:{args}")
    log.info(f"Platform:{platform.system()}")
    conf = load_config()
    if conf is None:
        log.error(f"start sync block failed:config is None")
        exit()
    check_args()
    kwargs = {
        "network": args.network.lower(),
        "target": args.target,
        "origin": args.origin,
        "node": args.node,
        "reload": args.reload,
        "delay": args.delay,
        "range": args.range
    }
    print(kwargs)
    task = Task(conf, **kwargs)
    task.run()

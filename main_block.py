# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from engine.block import Task
import argparse
import platform
from uitls import load_config
import logging as log

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
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


def check_args():
    if not args.network:
        log.error("network is None!")
        exit()
    if not args.node:
        log.error('node node in None!')
        exit()

    if args.reload is None:
        log.error('reload can not be none,must be True or False')
        exit()

    if args.origin < 0:
        log.error('block origin must > 0')
        exit()

    if args.interval <= 0:
        log.error('interval must > 0')
        exit()


if __name__ == '__main__':
    print(f"Args: {args}")
    print("platform:", platform.system())
    conf = load_config()
    if conf is None:
        log.error(f"start sync block failed:config is None")
        exit()
    check_args()
    kwargs = {
        "network": args.network.lower(),
        "origin": args.origin,
        "interval": args.interval,
        "node": args.node,
        "reload": args.reload
    }

    task = Task(conf, **kwargs)
    task.run()

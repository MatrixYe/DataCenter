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

from engine.oracle import Task
from utils import load_config

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
# 1区块网络
parser.add_argument("--network", type=str)
# 2 喂价源供应商，例如chainlink、uniswapv3
parser.add_argument("--provider", type=str)
# 3 喂价源合约地址
parser.add_argument("--target", type=str)
# 4 历史记录，默认0，不同步历史，从启动时刻开始同步
parser.add_argument("--history", type=int, default=0)
# 5 访问节点
parser.add_argument("--node", type=str, default=0)
# 6 消息推送地址
parser.add_argument("--webhook", type=str, default='')

args = parser.parse_args()


def check_args():
    if not args.network:
        log.error("network is None!")
        exit()
    if not args.provider:
        log.error("provider is None!")
        exit()
    if not args.target:
        log.error('target is None')
        exit()
    if not args.node:
        log.error('node node in None!')
        exit()
    if args.history > 5000 or args.history < 0:
        log.error("history must in [0,5000]")


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
        "provider": args.provider,
        "target": args.target,
        "history": args.history,
        "node": args.node,
        "webhook": args.webhook,
    }
    print(kwargs)
    task = Task(conf, **kwargs)
    task.run()

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

from engine.block import Task
from utils import load_config

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
# 区块网络
parser.add_argument("--network", type=str, default='')
# 起始点
parser.add_argument("--origin", type=int, default=0)
# 扫描周期
parser.add_argument("--interval", type=int, default=10)
# 连接节点
parser.add_argument("--node", type=str, default='')
# 消息推送地址
parser.add_argument("--webhook", type=str, default='None')

args = parser.parse_args()


def check_args():
    if not args.network:
        log.error("network is None!")
        exit()
    if not args.node:
        log.error('node node in None!')
        exit()

    if args.origin < 0:
        log.error(f'block origin must >= 0 ,but is {args.origin}')
        exit()

    if args.interval <= 0:
        log.error('interval must > 0')
        exit()


if __name__ == '__main__':
    log.info(f"Args Input:{args}")
    log.info(f"platform:{platform.system()}")
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
        "webhook": args.webhook
    }
    print(kwargs)
    task = Task(conf, **kwargs)
    task.run()

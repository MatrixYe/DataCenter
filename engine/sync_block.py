# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import argparse
import logging as log
import time

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--network", type=str)
parser.add_argument("--origin", type=int)
parser.add_argument("--rpc", type=str)
parser.add_argument("--interval", type=int)
parser.add_argument("--reload", type=str)

args = parser.parse_args()


class Task(object):
    def __init__(self, **kwargs):
        self.network = kwargs.get("network")
        self.origin = int(kwargs.get("origin"))
        self.rpc = kwargs.get("rpc")
        self.reload = kwargs.get("reload")
        self.interval = kwargs.get("interval")
        print(self.__dict__)

    def run(self):
        ok, err = self._check()
        if not ok:
            log.error(msg=f"can not run sync block:{err}")
            return
        for i in range(100):
            time.sleep(self.interval)
            log.debug(
                f"start sync block:network:{self.network} origin:{self.origin} reload:{self.reload} rpc:{self.rpc}")

    def _check(self) -> (bool, str):
        if not self.network:
            return False, "network is None!"
        if not self.rpc:
            return False, 'rpc node in None!'
        if self.reload is None:
            return False, 'reload can not be none,must be True or False'
        if self.origin <= 0:
            return False, 'block origin must > 0'
        return True, ""


if __name__ == '__main__':
    task = Task(network=args.network, origin=args.origin, interval=args.interval, rpc=args.rpc, reload=args.reload)
    task.run()

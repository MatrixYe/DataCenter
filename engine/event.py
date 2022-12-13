# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as log
import time

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


class Task(object):
    def __init__(self, **kwargs):
        self.network = kwargs.get("network")
        self.target = kwargs.get("target")
        self.origin = kwargs.get("origin")
        self.node = kwargs.get("node")
        self.reload = kwargs.get("reload")
        print(self.__dict__)

    def run(self):
        ok, err = self._check()
        if not ok:
            log.error(msg=f"can not run sync block:{err}")
            return
        for i in range(100):
            time.sleep(self.interval)
            log.debug(f"sync block:network:{self.network} origin:{self.origin} reload:{self.reload} node:{self.node}")

    def _check(self) -> (bool, str | None):
        if not self.network:
            return False, "network is None!"
        if not self.node:
            return False, 'node node in None!'
        if self.reload is None:
            return False, 'reload can not be none,must be True or False'
        if self.origin <= 0:
            return False, 'block origin must > 0'
        if self.interval <= 0:
            return False, 'interval must > 0'
        return True, None

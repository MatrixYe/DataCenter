# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import logging as _log

_log.basicConfig(level=_log.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def debug(msg: str):
    _log.debug(msg=msg)


def warn(msg: str):
    _log.warning(msg)


def error(msg: str):
    _log.error(msg=msg)

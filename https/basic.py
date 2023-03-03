# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Any


@dataclass
class Reply(object):
    code: int
    data: Any
    msg: str

    @classmethod
    def suc(cls, data):
        return cls(200, data, "success")

    @classmethod
    def err(cls, msg="undefined error message"):
        return cls(0, None, msg=msg)

    @classmethod
    def com(cls, data, msg=None):
        return cls.suc(data) if data else cls.err(msg)

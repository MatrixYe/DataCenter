# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import logging as log
import urllib.parse
from typing import List, Optional, Any

from pymongo import MongoClient

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s: -%(filename)s[L:%(lineno)d] %(message)s')


# noinspection PyBroadException
class MongoApi(object):
    def __init__(self, host='localhost', port=27017, user=None, password=None, db=None):
        user = urllib.parse.quote_plus(user)
        password = urllib.parse.quote_plus(password)
        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/?authMechanism=DEFAULT")
        self.database = self.client[db]
        # self.session = self.client.start_session()

    @classmethod
    def from_conf(cls, **kwargs):
        host = kwargs.get('host')
        port = kwargs.get('port')
        user = kwargs.get('user')
        password = kwargs.get('password')
        db = kwargs.get('db')
        parmas = dict()
        if host:
            parmas['host'] = host
        if port:
            parmas['port'] = port
        if user:
            parmas['user'] = user
        if password:
            parmas['password'] = password
        if db:
            parmas['db'] = db
        return cls(**parmas)

    def add_test_data(self, value):
        result = self.database.test.insert_one(value)
        return result

    def insert(self, colle: str, data=None) -> bool:
        if data is None:
            log.warning("data is None,skip insert")
            return True
        try:
            self.database[colle].insert_one(data)
            return True
        except BaseException as e:
            log.error(f"insert data failed:{e}")
            return False

    def drop(self, colle: str):
        if self.database[colle] is None:
            return
        self.database[colle].drop()

    def list_colle_names(self) -> List[str]:
        return self.database.list_collection_names()

    def colle_exist(self, c: str) -> bool:
        return c in self.list_colle_names()

    def find_one(self, c: str, filte: Optional[Any]):
        var = self.database[c]
        if var is None:
            return None
        else:
            return var.find_one(filter=filte)

    def find_all(self, c: str, filteit=None, sort_keys=None):
        var = self.database[c]
        if var is None:
            return None
        if not sort_keys:
            return var.find(filteit)
        else:
            return var.find(filteit).sort(sort_keys)

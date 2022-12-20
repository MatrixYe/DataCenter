# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import logging as log
import urllib.parse

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

    def insert(self, colle: str, data=None):
        if data is None:
            log.warning("data is None,skip insert")
        try:
            self.database[colle].insert_one(data)
        except BaseException as e:
            log.error(f"insert data failed:{str(e)}")

    def drop(self, colle: str):
        if self.database[colle] is None:
            return
        self.database[colle].drop()

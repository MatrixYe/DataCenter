# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from pymongo import MongoClient


class MongoApi(object):
    def __init__(self, host='localhost', port=27017, user=None, password=None, db='admim'):
        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/?authMechanism=DEFAULT")
        self.database = self.client[db]

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

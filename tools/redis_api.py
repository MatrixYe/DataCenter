# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import os
import json
import logging

from redis import StrictRedis


class RedisApi(object):

    def __init__(self, host='localhost', port=6379, password=None, db=0):
        self.redis = StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        self.ps = self.redis.pubsub(ignore_subscribe_messages=True)
        self.__setSubscribed = set()
        self.active = False
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)

    @classmethod
    def from_default(cls):
        params = dict()
        params['host'] = 'localhost'
        params['port'] = 6379
        params['password'] = None
        params['db'] = 0

        return cls(**params)

    @classmethod
    def from_config(cls, **kwargs):
        if not kwargs:
            return cls.from_default()

        host = kwargs.get('host')
        port = kwargs.get('port')
        pwd = kwargs.get('password')
        db = kwargs.get('db')

        params = dict()
        if pwd:
            params['password'] = pwd
        if host:
            params['host'] = host
        if port:
            params['port'] = port
        if db is not None:
            params['db'] = db

        return cls(**params)

    def start(self):
        self.active = True
        self.ps_thread = self.ps.run_in_thread(sleep_time=1)
        self.ps_thread.run()

    def stop(self):
        self.active = False
        self.ps_thread.stop()
        self.log.info("Stop Redis Api")

    def get(self, name):
        return self.redis.get(name)

    def set(self, name, value):
        return self.redis.set(name, value)

    def delele(self, name):
        return self.redis.delete(name)

    def hmset(self, name, value):
        return self.redis.hmset(name, value)

    def sub(self, channel_, callback, get_when_sub_=False):
        if self.active:
            self.log.error("Please subscribe channel before activating redis subscriber")

        new_sub = False
        if channel_ not in self.__setSubscribed:
            self.log.info("subscribe redis %s" % channel_)
            self.ps.subscribe(**{channel_: callback})
            new_sub = True

        self.__setSubscribed.add(channel_)

        if get_when_sub_:
            data = self.get(channel_)
            if data:
                msg = {
                    'channel': channel_,
                    'data': data,
                    'type': 'message'
                }
                callback(msg)
            return new_sub

    def un_sub(self, channel_):
        if channel_ not in self.__setSubscribed:
            self.log.info("redis %s not subscribed" % channel_)
        else:
            self.ps.unsubscribe(channel_)
            self.__setSubscribed.remove(channel_)

    def restart(self):
        self.log.info("Restart redis")
        self.stop()
        self.start()

    def pub(self, name, value):
        self.redis.publish(name, value)

    def pub_set(self, name, value):
        self.set(name, value)
        self.pub(name, value)

    def exists(self, name):
        return self.redis.exists(name)

    def expire(self, name, time):
        return self.redis.expire(name, time)

    def zadd(self, name, *args, **kwargs):
        return self.redis.zadd(name, *args, **kwargs)

    def zscore(self, name, value):
        return self.redis.zscore(name, value)

    def zrem(self, name, *values):
        return self.redis.zrem(name, *values)

    def get_redis_data(self, key):
        data_str = self.get(key)
        if data_str is None:
            return None
        else:
            return json.loads(data_str)

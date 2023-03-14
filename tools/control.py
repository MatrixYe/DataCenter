# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from typing import Union

from docker.models.containers import Container

import utils
from .docker_api import DockerApi
from .mongo_api import MongoApi
from .redis_api import RedisApi

IMG_SYNC_EVENT = "sync-event:latest"
IMG_SYNC_BLOCK = "sync-block:latest"
IMG_SYNC_ORACLE = "sync-oracle:latest"


class _Ctrl(object):
    def _conn_redis(self) -> RedisApi:
        """
        连接redis
        :return: redis client
        """
        redis_conf = self.conf['redis']['outside'] if utils.is_dev_env() else self.conf['redis']['inside']
        return RedisApi.from_config(**redis_conf)

    def _conn_mongo(self) -> MongoApi:
        """
        连接mongo
        :return: mongodb client
        """
        c = self.conf['mongo']['outside'] if utils.is_dev_env() else self.conf['mongo']['inside']
        return MongoApi.from_conf(**c)

    # noinspection PyMethodMayBeStatic
    def _conn_docker(self) -> DockerApi:
        """
        连接docker control
        :return: docker client
        """
        return DockerApi.from_env()

    def __init__(self, conf: dict):
        self.conf = conf
        self.docker: DockerApi = self._conn_docker()
        self.redis: RedisApi = self._conn_redis()
        self.mongo: MongoApi = self._conn_mongo()


class BlockCtrl(_Ctrl):
    def __init__(self, conf):
        super().__init__(conf)

    def _start_sync_block(self, c_name, c_net, c_env, c_restart) -> Union[Container, None]:
        container, _ = self.docker.run_container(image=IMG_SYNC_BLOCK,
                                                 name=c_name,
                                                 network=c_net,
                                                 volumes=None,
                                                 ports=None,
                                                 environment=c_env, restart=c_restart, commond=None)
        return container

    def _drop_block_data(self, network):
        table_name = utils.gen_block_table_name(network)
        tag_block = utils.gen_block_tag(network)
        self.mongo.drop(table_name)
        self.redis.delele(tag_block)

    # 开始同步block区块高度
    def start_block(self, network: str, origin: int, interval: int, node: str, webhook: str) -> (Container, str):
        """
        新增同步block链,运行容器
        :param network:
        :param origin:
        :param interval:
        :param node:
        :param webhook:
        :return:
        """
        c_net = utils.load_docker_net()
        c_name = utils.gen_block_continal_name(network=network)
        c_restart = {"Name": "always"}
        c_env = {
            "NETWORK": network,
            "ORIGIN": origin,
            "INTERVAL": interval,
            "NODE": node,
            "WEBHOOK": webhook,
        }

        old_container = self.docker.get_container(c_name)
        # 容器不存在->创建
        if old_container is None:
            print("container is not exist --> creating")
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            self._logs('start', {'network': network,
                                 'origin': origin,
                                 'interval': interval,
                                 'node': node,
                                 'webhook': webhook},
                       'create' if new_container else 'failed')
            return (new_container, 'create') if new_container else (None, 'failed')
        # 容器存在+运行状态+不重启 -> 跳过
        elif old_container.status == 'running':
            self._logs('start', {'network': network,
                                 'origin': origin,
                                 'interval': interval,
                                 'node': node,
                                 'webhook': webhook},
                       'pass')
            return old_container, 'pass'

        # 容器存在+停止状态+不重启 -> 移除+创建
        else:
            self.remove_block(network, clear=False)
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            self._logs('start', {'network': network,
                                 'origin': origin,
                                 'interval': interval,
                                 'node': node,
                                 'webhook': webhook},
                       'remove|create' if new_container else 'failed')
            return (new_container, 'remove|create') if new_container else (None, 'failed')

    def restart_block(self, network: str, origin: int, interval: int, node: str, webhook: str, clear=False):
        c_net = utils.load_docker_net()
        c_name = utils.gen_block_continal_name(network=network)
        c_restart = {"Name": "always"}
        c_env = {
            "NETWORK": network,
            "ORIGIN": origin,
            "INTERVAL": interval,
            "NODE": node,
            "WEBHOOK": webhook,
        }
        old_container = self.docker.get_container(c_name)
        # 容器不存在->创建
        if old_container is None:
            print("container is not exist --> creating")
            if clear:
                self._drop_block_data(network)
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)

            _act = 'create' if new_container else 'failed'
            self._logs('restart',
                       {
                           'network': network,
                           'origin': origin,
                           'interval': interval,
                           'node': node,
                           'webhook': webhook,
                           'clear': clear
                       },
                       _act
                       )
            return new_container, _act
        # 容器存在
        else:
            self.remove_block(network, clear=clear)
            new_container = self._start_sync_block(c_name, c_net, c_env, c_restart)
            _act = 'remove|clear|create' if clear else 'remove|create'
            self._logs('restart',
                       {
                           'network': network,
                           'origin': origin,
                           'interval': interval,
                           'node': node,
                           'webhook': webhook,
                           'clear': clear
                       },
                       _act
                       )
            return (new_container, _act) if new_container else (None, 'failed')

    # 停止同步block data
    def remove_block(self, network: str, clear: bool) -> (str, str):
        """
        停止block 同步
        :param network: 需要停止的网络
        :param clear:
        :return:
        """
        container_name = utils.gen_block_continal_name(network)
        container = self.docker.get_container(container_name)
        ret_act = ''
        if container is None:
            ret_act += 'noexist|pass'
        else:
            _, _ = self.docker.remove_container(container_name, force=True)
            ret_act += 'remove'
        if clear:
            self._drop_block_data(network)
            ret_act += '|clear'
        self._logs('remove', {'network': network, 'container': container_name, 'clear': clear}, ret_act)
        return container_name, ret_act

    # 获取最新同步的block高度
    def last_block(self, network) -> Union[dict, None]:
        tag = utils.gen_block_tag(network)
        return self.redis.getdict(tag)

    def _logs(self, ack, data, result=None):
        info = {
            "topic": "block",
            "action": ack,
            "data": data,
            "result": result,
            'time': utils.now()
        }
        self.mongo.insert("logs", info)

    # def _logs(self, topic, data):
    def task_info(self):
        cs = self.docker.all_container()
        buff = []
        for c in cs:
            #  容器名
            c_name = c.name
            if 'block-' not in c_name:
                continue
            # 环境变量
            es = c.attrs['Config']['Env']
            ed = dict()
            for e in es:
                iterm = e.split('=')
                ed[iterm[0]] = iterm[1]
            buff.append({
                'name': c_name,
                'args': {
                    'network': ed.get('NETWORK'),
                    'origin': ed.get('ORIGIN'),
                    'interval': ed.get('INTERVAL'),
                    'node': ed.get('NODE'),
                    'webhook': ed.get('WEBHOOK'),
                },
                'current_block': self.redis.getdict(utils.gen_block_tag(ed.get("NETWORK"))),
                'status': c.status
            })

        return buff


class EventCtrl(_Ctrl):
    def __init__(self, conf):
        super().__init__(conf)

    def _start_event(self, c_name, c_net, c_env, c_restart) -> Union[Container, None]:
        container, _ = self.docker.run_container(image=IMG_SYNC_EVENT,
                                                 name=c_name,
                                                 network=c_net,
                                                 volumes=None,
                                                 ports=None,
                                                 environment=c_env,
                                                 restart=c_restart,
                                                 commond=None)
        return container

    def _log(self, act, data, result=None):
        self.mongo.insert('logs', {
            'topic': 'event',
            'action': act,
            'data': data,
            'result': result,
            'time': utils.now()
        })

    def start_event(self, network, target, origin, node, delay, ranger, webhook) -> (Container, str):
        c_net = utils.load_docker_net()
        c_name = utils.gen_event_container_name(network=network, target=target)
        c_restart = {"Name": "always"}
        c_env = {
            "NETWORK": network,
            "TARGET": target,
            "ORIGIN": origin,
            "NODE": node,
            "DELAY": delay,
            "RANGE": ranger,
            "WEBHOOK": webhook,
        }
        old_container = self.docker.get_container(c_name)
        # 容器不存在->创建
        if old_container is None:
            print("container is not exist --> creating")
            new_container = self._start_event(c_name, c_net, c_env, c_restart)

            self._log('start', {'network': network,
                                'target': target,
                                'origin': origin,
                                'node': node,
                                'delay': delay,
                                'ranger': ranger,
                                'webhook': webhook},
                      'create' if new_container else 'failed')
            return (new_container, 'create') if new_container else (None, 'failed')
        # 容器存在+运行状态 -> 跳过
        elif old_container.status == 'running':
            self._log('start', {'network': network,
                                'target': target,
                                'origin': origin,
                                'node': node,
                                'delay': delay,
                                'ranger': ranger,
                                'webhook': webhook},
                      'pass')
            return old_container, 'pass'
        # 容器存在+停止状态+不重启 -> 移除+创建
        else:
            self.remove_event(network, target, delete=False)
            new_container = self._start_event(c_name, c_net, c_env, c_restart)
            self._log('start', {'network': network,
                                'target': target,
                                'origin': origin,
                                'node': node,
                                'delay': delay,
                                'ranger': ranger,
                                'webhook': webhook},
                      'remove|create' if new_container else 'failed')
            return (new_container, 'remove|create') if new_container else (None, 'failed')

    def restart_event(self, network, target, origin, node, delay, ranger, webhook, cleardb):
        c_net = utils.load_docker_net()
        c_name = utils.gen_event_container_name(network=network, target=target)
        c_restart = {"Name": "always"}
        c_env = {
            "NETWORK": network,
            "TARGET": target,
            "ORIGIN": origin,
            "NODE": node,
            "DELAY": delay,
            "RANGE": ranger,
            "WEBHOOK": webhook,
        }
        old_container = self.docker.get_container(c_name)
        # 容器不存在->创建
        if old_container is None:
            print("container is not exist --> creating")
            if cleardb:
                self._drop_event_data(network, target)
            new_container = self._start_event(c_name, c_net, c_env, c_restart)
            self._log('start', {'network': network,
                                'target': target,
                                'origin': origin,
                                'node': node,
                                'delay': delay,
                                'ranger': ranger,
                                'webhook': webhook,
                                'clear': cleardb},
                      'create' if new_container else 'failed')
            return (new_container, 'create') if new_container else (None, 'failed')
        # 容器存在+停止状态+不重启 -> 移除+创建
        else:
            self.remove_event(network, target, delete=cleardb)
            new_container = self._start_event(c_name, c_net, c_env, c_restart)
            self._log('start', {'network': network,
                                'target': target,
                                'origin': origin,
                                'node': node,
                                'delay': delay,
                                'ranger': ranger,
                                'webhook': webhook},
                      'remove|create' if new_container else 'failed')
            return (new_container, 'remove|create') if new_container else (None, 'failed')

    def _drop_event_data(self, network, target):
        table_name = utils.gen_event_table_name(network, target)
        tag_block = utils.gen_event_tag(network, target)
        self.mongo.drop(table_name)
        self.redis.delele(tag_block)

    def remove_event(self, network, target, delete):
        container_name = utils.gen_event_container_name(network, target)
        container = self.docker.get_container(container_name)
        ret_act = ''
        if container is None:
            ret_act += '|noexist|pass'
        else:
            _, _ = self.docker.remove_container(container_name, force=True)
            ret_act += '|remove'
        if delete:
            self._drop_event_data(network, target)
            ret_act += '|clear'
        self._log('start', {'network': network,
                            'target': target,
                            'delete': delete},
                  ret_act)
        return container_name, ret_act

    def last_event(self, network, target):
        tag = utils.gen_event_tag(network, target)
        return self.redis.getdict(tag)

    def task_info(self):
        cs = self.docker.all_container()
        buff = []
        for c in cs:
            #  容器名
            c_name = c.name
            if 'event-' not in c_name:
                continue
            # 环境变量
            es = c.attrs['Config']['Env']
            ed = dict()
            for e in es:
                iterm = e.split('=')
                ed[iterm[0]] = iterm[1]
            buff.append({
                'name': c_name,
                'args': {
                    'network': ed.get('NETWORK'),
                    'target': ed.get('TARGET'),
                    'origin': ed.get('ORIGIN'),
                    'node': ed.get('NODE'),
                    'delay': ed.get('DELAY'),
                    'range': ed.get('RANGE'),
                    'webhook': ed.get('WEBHOOK'),
                },
                'current_event': self.redis.getdict(utils.gen_block_tag(ed.get("NETWORK"))),
                'status': c.status
            })

        return buff

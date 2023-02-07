# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from concurrent import futures

import grpc

import utils
from pb import server_pb2_grpc, server_pb2
from tools.docker_api import DockerApi
from tools.mongo_api import MongoApi
from tools.redis_api import RedisApi
from .ctrl import Ctrl


class DataCenterImp(server_pb2_grpc.DataCenterServicer):
    def __init__(self, redis, mongo, docker):
        self.redis: RedisApi = redis
        self.mongo: MongoApi = mongo
        self.docker: DockerApi = docker
        self.control = Ctrl(redis=redis, mongo=mongo, docker=docker)

    @staticmethod
    def _error(context, code, msg):
        context.set_code(code)
        context.set_details(msg)

    @staticmethod
    def _gen_data(event):
        return {
            'sender': event['sender'],
            'itype': event['itype'],
            'bvalue': event['bvalue'],
            'block_number': event['block_number'],
            'index': event['index'],
            'tx_hash': event['tx_hash']
        }
        pass

    # 获取最新区块高度
    def BlockLast(self, request, context):
        network = request.network
        tag = utils.gen_block_cache_name(network=network)
        h = self.redis.get(tag)
        if h is None:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.BlockLastReply()
        else:
            return server_pb2.BlockLastReply(height=int(h))

    # 获取区块详情
    def BlockDetail(self, request, context):
        network = request.network
        height = request.height
        # target_colle = f"block_{network}"
        target_colle = utils.gen_block_table_name(network=network)
        target_id = height
        detail = self.mongo.find_one(target_colle, {'_id': target_id})
        if not detail:
            self._error(context, grpc.StatusCode.NOT_FOUND, "未找到相关区块，请检查网络或高度是否正确")
            return server_pb2.BlockDetailReply()
        else:
            timestamp = detail['timestamp']
            hashs = detail['hash']
            return server_pb2.BlockDetailReply(network=network, height=height, timestamp=timestamp, hash=hashs)

    # 获取raw event最新同步高度
    def EventLast(self, request, context):
        network = request.network
        target = request.target
        if not utils.is_address(target):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "目标地址为Null或者地址长度错误")
            return server_pb2.EventLastReply()
        tag = utils.gen_event_cache_name(network=network, target=target)
        h = self.redis.get(name=tag)
        if not h:
            self._error(context, grpc.StatusCode.NOT_FOUND, "未找到最新同步高度，请检查网络名称或目标地址是否正确")
            return server_pb2.EventLastReply()
        return server_pb2.EventLastReply(height=int(h))

    def EventFilter(self, request, context):
        #   string network = 1;
        #   string target = 2;
        #   uint64 start = 3;
        #   uint64 end = 4;
        #   repeated string senders = 5;
        #   repeated int32 itypes = 6;
        network = request.network
        target = request.target
        start = request.start
        end = request.end
        senders = list(request.senders)
        desc = request.desc
        print(f"接收到参数:{network} {target} {start} {end} {senders} {desc}")
        if not utils.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.EventFilterReply()
        if not utils.is_address(target):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "目标地址为非法")
            return server_pb2.EventFilterReply()
        if start <= 0 or end <= 0 or start > end:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "查询高度范围错误，start > end")
            return server_pb2.EventFilterReply()
        colle = utils.gen_event_table_name(network=network, target=target)
        if senders:
            events = self.mongo.find_all(colle,
                                         {
                                             'sender': {'$in': senders},
                                             'block_number': {'$gte': start, '$lte': end}
                                         }, desc
                                         )
        else:
            events = self.mongo.find_all(colle, {'block_number': {'$gte': start, '$lte': end}}, desc)

        datas = [self._gen_data(e) for e in list(events)] if events else []
        return server_pb2.EventFilterReply(events=datas)

    def OraclePrice(self, request, context):
        return super().OraclePrice(request, context)

    def OraclePriceChg(self, request, context):
        return super().OraclePriceChg(request, context)

    def OracleData(self, request, context):
        return super().OracleData(request, context)

    def StartSyncBlock(self, request, context):
        network = request.network
        origin = request.origin
        interval = request.interval
        node = request.node
        webhook = request.webhook
        if not utils.check_network(network):
            msg = f"无法识别的区块网络{network}"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if origin < 0:
            msg = "block同步起始点必须 >= 0 (为零时从当前区块高度开始同步)"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if interval <= 0 or interval > 600:
            msg = "interval 必须位于区间[0,600]"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if not node:
            msg = "无法识别的node节点"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)
        if not webhook:
            webhook = 'None'
        # network: str, origin: int, interval: int, node: str, webhook: str
        msg = self.control.start_sync_block(network, origin, interval, node, webhook)
        return server_pb2.ComReply(result='SUCCESS', msg=msg)

    def StopSyncBlock(self, request, context):
        #   string network = 1;
        network = request.network
        delete = request.delete
        if not utils.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.ComReply()
        msg = self.control.stop_sync_block(network, delete)
        return server_pb2.ComReply(result="SUCCESS", msg=msg)

    def StartSyncEvent(self, request, context):
        network = request.network
        target = request.target
        origin = request.origin
        node = request.node
        delay = request.delay
        ranger = request.range
        webhook = request.webhook
        if not utils.check_network(network):
            msg = f"无法识别的区块网络{network}"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if not utils.is_address(target):
            msg = f"目标地址错误:{target}"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if origin <= 0:
            msg = "Event同步起始点必须 >= 0"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if not node:
            msg = "无法识别的远程节点Node"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if delay < 0 or delay > 5:
            msg = "同步高度延时必须 >=0 & <=5"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        if ranger < 100 or ranger > 10000:
            msg = f"ranger 的合法区间为[100,10000]"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)
        if not webhook:
            webhook = 'None'
        # network: str, target: str, origin: int, node: str, delay: int, ranger: int,webhook: str
        msg = self.control.start_sync_event(network, target, origin, node, delay, ranger, webhook)
        return server_pb2.ComReply(result='SUCCESS', msg=msg)

    def StopSyncEvent(self, request, context):
        network = request.network
        target = request.target
        delete = request.delete
        if not utils.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.ComReply()

        if not utils.is_address(target):
            msg = f"无法识别的target：{target}"
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, msg)
            return server_pb2.ComReply(result='FAILED', msg=msg)

        #  network: str, target: str, delete: bool
        msg = self.control.stop_sync_event(network=network, target=target, delete=delete)
        return server_pb2.ComReply(result="SUCCESS", msg=msg)

    def StartSyncOracle(self, request, context):
        return super().StartSyncOracle(request, context)

    def StopSyncOracle(self, request, context):
        return super().StopSyncOracle(request, context)


class RpcServer(object):
    """
    Rpc Server
    """

    def __init__(self, conf, **kwargs):
        self.conf = conf
        self.port = kwargs.get('port')
        self.redis = self._conn_redis()
        self.mongo = self._conn_mongo()
        self.docker = self._conn_docker()

    def run(self):
        print("RPC 服务启动... ...")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # data_center = DataCenterImp(self.redis, self.mongo, self.docker_api),
        server_pb2_grpc.add_DataCenterServicer_to_server(DataCenterImp(self.redis, self.mongo, self.docker),
                                                         server)
        server.add_insecure_port(f'[::]:{self.port}')
        server.start()
        server.wait_for_termination()

    def _conn_redis(self) -> RedisApi:
        """
        连接redis
        :return: redis client
        """
        c = self.conf
        if utils.is_dev_env():
            return RedisApi.from_config(**c['redis']['outside'])
        else:
            return RedisApi.from_config(**c['redis']['inside'])

    def _conn_mongo(self) -> MongoApi:
        """
        连接mongo
        :return: mongodb client
        """
        c = self.conf
        if utils.is_dev_env():
            return MongoApi.from_conf(**c['mongo']['outside'])
        else:
            return MongoApi.from_conf(**c['mongo']['inside'])

    # noinspection PyMethodMayBeStatic
    def _conn_docker(self) -> DockerApi:
        """
        连接docker control
        :return: docker client
        """
        return DockerApi.from_env()

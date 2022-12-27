# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from pb import server_pb2_grpc, server_pb2
from concurrent import futures
import grpc

from tools.redis_api import RedisApi
from tools.mongo_api import MongoApi
from tools.docker_api import DockerApi
from uitls import is_dev_env

from . import ctrl

NETWORKS = {
    "MAINNET": 1,
    "ROPSTEN": 3,
    "RINKEBY": 4,
    "GOERLI": 5,
    "KOVAN": 42,
    "MATIC": 137,
    "MATIC_TESTNET": 80001,
    "FANTOM": 250,
    "FANTOM_TESTNET": 4002,
    "XDAI": 100,
    "BSC": 56,
    "BSC_TESTNET": 97,
    "ARBITRUM": 42161,
    "ARBITRUM_TESTNET": 79377087078960,
    "MOONBEAM_TESTNET": 1287,
    "AVALANCHE": 43114,
    "AVALANCHE_TESTNET": 43113,
    "HECO": 128,
    "HECO_TESTNET": 256,
    "HARMONY": 1666600000,
    "HARMONY_TESTNET": 1666700000,
    "OKEX": 66,
    "OKEX_TESTNET": 65,
    "CELO": 42220,
    "PALM": 11297108109,
    "PALM_TESTNET": 11297108099,
    "MOONRIVER": 1285,
    "FUSE": 122,
}


class DataCenterImp(server_pb2_grpc.DataCenterServicer):
    def __init__(self, redis_api, mongo_api, docker_api):
        self.redis_api: RedisApi = redis_api
        self.mongo_api: MongoApi = mongo_api
        self.docker_api = docker_api
        pass

    @staticmethod
    def _error(context, code, msg):
        context.set_code(code)
        context.set_details(msg)
        pass

    # 获取最新区块高度
    def BlockLast(self, request, context):
        network = request.network
        tag = f"block_{network}_height"
        h = self.redis_api.get(tag)
        if h is None:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.BlockLastReply()
        else:
            return server_pb2.BlockLastReply(height=int(h))

    # 获取区块详情
    def BlockDetail(self, request, context):
        network = request.network
        height = request.height
        target_colle = f"block_{network}"
        target_id = height
        detail = self.mongo_api.find_one(target_colle, {'_id': target_id})
        if not detail:
            self._error(context, grpc.StatusCode.NOT_FOUND, "未找到相关区块，请检查网络或高度是否正确")

            return server_pb2.BlockDetailReply()
        else:
            timestamp = detail['timestamp']
            hashs = detail['hash']
            return server_pb2.BlockDetailReply(network=network, height=height, timestamp=timestamp, hash=hashs)

    # 获取raw event最新同步高度
    def EventLast(self, request, context):
        target = request.target
        if not target or len(target) <= 32:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "目标地址为Null或者地址长度错误")
            return server_pb2.EventLastReply()
        tag = f"event_{target[2:6]}_{target[-4:]}"
        h = self.redis_api.get(name=tag)
        if not h:
            self._error(context, grpc.StatusCode.NOT_FOUND, "未找到最新同步高度，请检查网络名称或目标地址是否正确")
            return server_pb2.EventLastReply()

        return server_pb2.EventLastReply(height=int(h))

    @staticmethod
    def check_network(network):
        if network.upper() not in NETWORKS.keys():
            return False
        else:
            return True

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
        # print(f"接收到参数:{network} {target} {start} {end} {senders}")
        if not self.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.EventFilterReply()
        if not target or len(target) < 32:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "目标地址为Null或者长度错误")
            return server_pb2.EventFilterReply()
        if start < 0 or end < 0 or start >= end:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "查询高度范围错误，start must < end")
            return server_pb2.EventFilterReply()
        colle = f"event_{target[2:6]}_{target[-4:]}"
        events = self.mongo_api.find_all(colle,
                                         {
                                             'sender':
                                                 {
                                                     '$in': senders
                                                 },
                                             'block_number':
                                                 {
                                                     '$gte': start,
                                                     '$lte': end
                                                 }
                                         })

        datas = [{'sender': a['sender'],
                  'itype': a['itype'],
                  'bvalue': a['bvalue'],
                  'block_number': a['block_number'],
                  'index': a['index'],
                  'tx_hash': a['tx_hash']} for a in list(events)]
        # for i, data in enumerate(datas):
        #     print(data)
        return server_pb2.EventFilterReply(events=datas)

    def OraclePrice(self, request, context):
        return super().OraclePrice(request, context)

    def OraclePriceChg(self, request, context):
        return super().OraclePriceChg(request, context)

    def OracleKline(self, request, context):
        return super().OracleKline(request, context)

    def StartSyncBlock(self, request, context):
        #   string network = 1;
        #   uint64 origin = 2;
        #   uint32 interval = 3;
        #   string node = 4;
        #   bool reload = 5;
        network = request.network
        origin = request.origin
        interval = request.interval
        node = request.node
        reload = request.reload
        if not self.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.ComReply()

        if origin < 0:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT,
                        "block同步起始点必须 >= 0 (为零时从当前区块高度开始同步)")
            return server_pb2.ComReply(result='FAILED', msg='')

        if interval <= 0 or interval > 600:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT,
                        "扫描周期必须 >0")
            return server_pb2.ComReply(result='FAILED', msg='')

        if not node:
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT,
                        "无法识别的Node节点")
            return server_pb2.ComReply(result='FAILED', msg='')

        # network: str, origin: int, interval: int, node: str, reload: bool
        msg = ctrl.run_sync_block_container(network, origin, interval, node, reload)
        return server_pb2.ComReply(result='SUCCESS', msg=msg)

    def StopSyncBlock(self, request, context):
        #   string network = 1;
        network = request.network
        if not self.check_network(network):
            self._error(context, grpc.StatusCode.INVALID_ARGUMENT, "未识别的区块网络")
            return server_pb2.ComReply()
        msg = ctrl.rm_sync_block_container(network)

        return server_pb2.ComReply(result="SUCCESS", msg=msg)

    def StartSyncEvent(self, request, context):

        return super().StartSyncEvent(request, context)

    def StopSyncEvent(self, request, context):
        return super().StopSyncEvent(request, context)

    def StartSyncOracle(self, request, context):
        return super().StartSyncOracle(request, context)

    def StopSyncOracle(self, request, context):
        return super().StopSyncOracle(request, context)


# def Start(conf, port):
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     server_pb2_grpc.add_DataCenterServicer_to_server(DataCenterImp(), server)
#     server.add_insecure_port(f'[::]:{port}')
#     server.start()
#     server.wait_for_termination()


class RpcServer(object):
    def __init__(self, conf, **kwargs):
        self.conf = conf
        self.port = kwargs.get('port')
        self.redis_api = self._conn_redis()
        self.mongo_api = self._conn_mongo()
        self.docker_api = self._conn_docker()

    def run(self):
        print("RPC 服务启动... ...")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_DataCenterServicer_to_server(DataCenterImp(self.redis_api, self.mongo_api, self.docker_api),
                                                         server)
        server.add_insecure_port(f'[::]:{self.port}')
        server.start()
        server.wait_for_termination()

    def _conn_redis(self) -> RedisApi:
        c = self.conf
        if is_dev_env():
            return RedisApi.from_config(**c['redis']['outside'])
        else:
            return RedisApi.from_config(**c['redis']['outside'])

    def _conn_mongo(self) -> MongoApi:
        c = self.conf
        if is_dev_env():
            return MongoApi.from_conf(**c['mongo']['outside'])
        else:
            return MongoApi.from_conf(**c['mongo']['outside'])

    def _conn_docker(self) -> DockerApi:
        return DockerApi.from_env()

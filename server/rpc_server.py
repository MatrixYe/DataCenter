# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import grpc
from . import server_pb2, server_pb2_grpc


class AdminImp(server_pb2_grpc.AdminServicer):
    def __int__(self):
        pass

    def StartSyncBlock(self, request, context):
        return super().StartSyncBlock(request, context)


class ServerImp(server_pb2_grpc.MasterServicer):
    def __int__(self):
        pass

    def BlockLast(self, request, context):
        return super().BlockLast(request, context)

    def BlockDetail(self, request, context):
        return super().BlockDetail(request, context)

    def EventLast(self, request, context):
        return super().EventLast(request, context)

    def EventFilter(self, request, context):
        return super().EventFilter(request, context)

    def OraclePrice(self, request, context):
        return super().OraclePrice(request, context)

    def OraclePriceChg(self, request, context):
        return super().OraclePriceChg(request, context)

    def OracleKline(self, request, context):
        return super().OracleKline(request, context)


def start():
    pass

# def start(host: str, port: int, **kwargs):
#     print(f"host={host} port={port}")
#     infos = docker_api.info()
#     pp.pprint(infos)
#     # --network
#     # bsc
#     # --origin
#     # 23836740
#     # --interval
#     # 2
#     # --node
#     # https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/
#     # --reload
#     # False
#
#     print("测试重新开始同步bsc")
#     ctrl.sync_block(network='bsc', origin=0, interval=2,
#                     node='https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/',
#                     reload=False)
#     time.sleep(100)

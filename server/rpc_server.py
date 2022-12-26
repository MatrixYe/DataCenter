# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from . import server_pb2_grpc, server_pb2
from concurrent import futures
import grpc
import time


class DataCenterImp(server_pb2_grpc.DataCenterServicer):
    def __int__(self):
        pass

    def BlockLast(self, request, context):
        network = request.network
        print(f"receive network={network}")
        return server_pb2.BlockLastReply(network=request.network, height=778899, timestamp=998877,
                                         hash='0xababababababab')

    def BlockDetail(self, request, context):
        return

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

    def StartSyncBlock(self, request, context):
        return super().StartSyncBlock(request, context)

    def StopSyncBlock(self, request, context):
        return super().StopSyncBlock(request, context)

    def StartSyncEvent(self, request, context):
        return super().StartSyncEvent(request, context)

    def StopSyncEvent(self, request, context):
        return super().StopSyncEvent(request, context)

    def StartSyncOracle(self, request, context):
        return super().StartSyncOracle(request, context)

    def StopSyncOracle(self, request, context):
        return super().StopSyncOracle(request, context)


def Start(host, port):
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # server_pb2_grpc.add_DataCenterServicer_to_server(DataCenterImp, server)
    # server.add_insecure_port(f'{host}:{port}')
    # print(f"host={host},port={port}")
    # server.wait_for_termination()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_DataCenterServicer_to_server(DataCenterImp(), server)
    server.add_insecure_port('[::]:9005')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from . import server_pb2_grpc as gr
import grpc
from concurrent import futures


class DataCenterImp(gr.DataCenterServicer):
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


def start(host, port):
    print(f"connect {host}:{port}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gr.add_DataCenterServicer_to_server(DataCenterImp, server)
    server.add_insecure_port(f'{host}:{port}')
    server.wait_for_termination()

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
from __future__ import print_function
import logging

import grpc
from server import server_pb2
from server import server_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:9005')
    stub = server_pb2_grpc.DataCenterStub(channel=channel)
    response = stub.BlockLast(server_pb2.BlockLastAsk(network='fuck you '))

    print(f"Greeter client received:{response.network} ")
    print(f"Greeter client received:{response.height} ")
    # response2 = stub.BlockDetail(server_pb2.BlockDetailAsk(height=9988))
    # print(response2)


if __name__ == '__main__':
    logging.basicConfig()
    run()

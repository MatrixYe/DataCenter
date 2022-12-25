# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import grpc
from server import server_pb2, server_pb2_grpc

_HOST = 'localhost'
_PORT = '9005'


def run():
    print("fuck y")
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = server_pb2_grpc.DataCenterStub(channel=conn)
    response = client.BlockLast(server_pb2.BlockLastAsk(network='bsc'))
    print(response)


if __name__ == '__main__':
    run()

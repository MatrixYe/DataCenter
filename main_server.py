# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import argparse
from server import rpc_server

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
parser.add_argument("--host", type=str, default='0.0.0.0')
parser.add_argument("--port", type=int, default=9005)
args = parser.parse_args()

if __name__ == '__main__':
    print("hello ,this is server")
    host = args.host
    port = args.port
    print(host, port)
    rpc_server.start(host, port)

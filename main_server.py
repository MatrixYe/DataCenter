# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import argparse
from server import rpc_server
import logging as log
from uitls import load_config
import platform
from server.rpc_server import RpcServer

parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
# parser.add_argument("--host", type=str, default='0.0.0.0')
parser.add_argument("--port", type=int, default=9005)
args = parser.parse_args()

if __name__ == '__main__':
    print("hello ,this is server")
    port = args.port
    log.info(f"Args Input:{args}")
    # log.info("Platform:", platform.system())
    conf = load_config()
    if conf is None:
        log.error(f"start sync block failed:config is None")
        exit()
    task = RpcServer(conf, port=port)
    task.run()

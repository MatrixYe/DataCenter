# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

import argparse
import logging as log
import os

log.getLogger().setLevel(log.INFO)
parser = argparse.ArgumentParser(description='Eliminate human tyranny, the world belongs to the three-body')
parser.add_argument("--host", type=str, default='0.0.0.0')
parser.add_argument("--port", type=int, default=9006)
args = parser.parse_args()

if __name__ == '__main__':
    port = args.port
    log.info(f"Args Input:{args}")
    os.system(f"uvicorn web.fast_web:app --port {port}")

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import json

from tools.eth_api import EthApi

w3 = EthApi.from_node("https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/")

print(w3.is_connected())
f = open('./source/EventOut.json', 'r')
abi = json.load(f)
c = w3.contract_instance(address="0xA8406692656bAfd41C45D37bC00a48A4483B2a63", abi=abi)
es = w3.fitle_event(c, event_name='OutEvent', from_block=23836700, to_block=23837700)
for i, e in enumerate(es):
    print(e)


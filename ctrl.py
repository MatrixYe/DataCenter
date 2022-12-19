# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os
from tools import docker_api
import uitls

CHAIN = {
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


def sync_block(network: str, origin: int, interval: int, node: str, reload: bool):
    net = uitls.load_docker_net()
    name = f"block-{network}"
    net_alias = f"{name}host"
    img = "sync-block"
    restart = "on-failure:3"
    st = docker_api.statu(name)
    if st == 0:
        print("container is not exist --> creating")
        cmd = f"docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE={node} -e RELOAD={reload} --network {net} --network-alias {net_alias} --restart={restart} {img}"
        os.system(cmd)
    if st == 1:
        print("container is exist --> pass")
    if st == -1:
        print("container is exist,but not running --> remove and creating")
        cmd1 = f"docker rm -f {name}"
        cmd2 = f"docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE={node} -e RELOAD={reload} --network {net} --network-alias {net_alias} --restart={restart} {img}"
        os.system(cmd1)
        os.system(cmd2)


def remove_block(network: str):
    name = f"block-{network}"
    st = docker_api.statu(name)
    if st == 0:
        print(f"container:{name} is not exist --> pass")
        pass
    if st == 1:
        print(f"container:{name} is  exist and running --> stop&remove")
        # cmd1 = f"docker stop {name}"
        cmd2 = f"docker rm -f {name}"
        # os.system(cmd1)
        os.system(cmd2)
    if st == -1:
        print(f"container:{name} is  exist and stoped --> remove")
        cmd = f"docker rm -f {name}"
        os.system(cmd)
    print("remove block success")


def sync_event():
    # todo
    pass


def sync_oracle():
    # todo
    pass


if __name__ == '__main__':
    # --network
    # bsc
    # --origin
    # 23836740
    # --interval
    # 2
    # --node
    # https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/
    # --reload
    # False
    sync_block(network='bsc',
               origin=23836740,
               interval=3,
               node='https://snowy-lively-log.bsc.discover.quiknode.pro/b2e8cf05409330a7788453776b6748fe6986389d/',
               reload=False)
    # time.sleep(10)
    # remove_block('bsc')
#

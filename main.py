import argparse
import logging as log
import time

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 接收输入参数
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--target", type=str)
parser.add_argument("--rpc", type=str)
args = parser.parse_args()


def run():
    for i in range(100):
        print(args.target)
        print(args.rpc)
        print('--' * 10)
        time.sleep(2)


if __name__ == '__main__':
    run()

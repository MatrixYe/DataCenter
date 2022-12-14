# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from tools import docker

# docker.pull_image('hello-world:latest')
print(docker.images())
print(docker.continers(flag=True))
docker.rm_container('center_redis', force=True)
docker.rm_image('hello-world', False)
docker.rm_image('conda/miniconda3:latest', True)
print(docker.continers(flag=True))
print(docker.images())

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------

from tools import docker_api

# docker_api.pull_image('hello-world:latest')
print(docker_api.images())
print(docker_api.continers(flag=True))
docker_api.rm_container('center_redis', force=True)
docker_api.rm_image('hello-world', False)
docker_api.rm_image('conda/miniconda3:latest', True)
print(docker_api.continers(flag=True))
print(docker_api.images())

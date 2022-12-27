# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os

import docker


class DockerApi(object):
    def __init__(self, client):
        self.client = client
        pass

    @classmethod
    def from_env(cls):
        c = docker.from_env()
        return cls(c)

    # 获取docker镜像列表
    def images(self) -> list:
        result = list()
        # 二级数组
        groups = [a.tags for a in self.client.images.list()]
        for group in groups:
            for image in group:
                result.append(image)
        return result

    # 获取docker网络列表
    def networks(self) -> list:
        return [a.name for a in self.client.networks.list()]

    # 创建docker网络
    def create_network(self, name: str):
        if name not in self.networks():
            print(f"network:{name} --> creating")
            self.client.networks.create(name)
        else:
            print(f"network:{name} is exited --> pass")

    # 获取docker容器列表
    def continers(self, flag=False) -> list:
        return [a.name for a in self.client.containers.list(all=flag)]

    # 获取docker挂载列表
    def volumes(self) -> list:
        return [a.name for a in self.client.volumes.list()]

    # 拉取docker镜像
    def pull_image(self, img_name: str):
        if img_name not in self.images():
            print(f"---> pull image:{img_name}")
            self.client.images.pull(img_name)
        else:
            print(f"image:{img_name} is exited --> pass")

    # 移除镜像
    def rm_image(self, img_name: str, force: bool):
        imgs = self.images()
        for _, img in enumerate(imgs):
            if img == img_name:
                img.remove(force=force)
                return
        print(f"image:{img_name} is not find ")

    # 移除容器
    def rm_container(self, name, force: bool):
        cs = self.client.containers.list(all=True)
        for i, c in enumerate(cs):
            if c.name == name or c.short_id == name:
                print(f"find container:{c.name} --> remove it")
                c.remove(force=force)
                return
        print(f"container:{name} is not finded")

    # 创建docker挂载
    def create_volume(self, name: str):
        # create volume
        if name not in self.volumes():
            print(f"volume :{name} --> creating")
            self.client.volumes.create(name)
        else:
            print(f"volume:{name} is exited --> pass")

    # 创建并运行redis容器
    def run_redis_container(self, name, port, network, network_alias, volume, restart, img, password):
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                print(f"container:{name} is exist bud not run --> remove it")
                os.system(f"docker rm {name}")
            print(f"container{name} --> creating")
            cmd = f"docker run -itd -p {port} --name {name} --network {network} --network-alias {network_alias} -v {volume}:/data --restart={restart} {img} --requirepass {password} "
            print(f"CMD: {cmd}")
            os.system(cmd)
        else:
            print(f"container:{name} is exist and is running --> pass")

    # 创建并运行postgrest容器
    def run_pg_container(self, name, port, network, network_alias, volume, user, password, restart, img):
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                os.system(f"docker rm {name}")
                print(f"container:{name} is exist and is stopped --> remove")
            print(f"container{name} --> creating")
            cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -v {volume}:/var/lib/postgresql/data -e POSTGRES_USER={user} -e POSTGRES_PASSWORD={password} -e ALLOW_IP_RANGE=0.0.0.0/0 --restart={restart} {img}"
            print(f"CMD: {cmd}")
            os.system(cmd)
        else:
            print(f"container:{name} is exist and is running --> pass")

    # 创建并运行mongodb容器
    def run_mongo_container(self, name, port, network, network_alias, volume, user, password, restart, img, cache,
                            memory,
                            memory_swap):
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                os.system(f"docker rm {name}")
                print(f"container:{name} is exist and is stopped --> remove")
            print(f"container:{name} --> creating")
            cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -m {memory} --memory-swap {memory_swap} -e MONGO_INITDB_ROOT_USERNAME={user} -e MONGO_INITDB_ROOT_PASSWORD={password} -v {volume}:/data/db --restart={restart} {img} --wiredTigerCacheSizeGB {cache}"
            print(f"CMD: {cmd}")
            os.system(cmd)
        else:
            print(f"container:{name} is exist and is running --> pass")

    def info(self):
        cs = self.client.containers.list(all=True)
        simp_cs = [{'name': a.name,
                    'short_id': a.image.short_id,
                    'image': {
                        'tags': a.image.tags,
                        'short_id': a.image.short_id
                    },
                    'ports': a.ports,
                    'status': a.status,
                    }
                   for a in cs]
        imgs = self.client.images.list()
        simp_imgs = [
            {
                'short_id': a.short_id,
                'tags': a.tags,
            } for a in imgs]
        return {
            'contianers': simp_cs,
            'images': simp_imgs
        }

    def statu(self, c_name: str) -> int:
        # - `status` (str): One of ``restarting``, ``running``,
        #                     ``paused``, ``exited``
        cs = self.client.containers.list(all=True)
        for c in cs:
            if c.name == c_name and c.status == 'running':
                return 1
            if c.name == c_name and c.status != 'running':
                return -1
        return 0

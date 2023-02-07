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
    """
    Docker Client Api
    """

    def __init__(self, client):
        self.client = client
        pass

    @classmethod
    def from_env(cls):
        c = docker.from_env()
        return cls(c)

    def images(self) -> list:
        """
        获取docker镜像列表
        :return:
        """
        result = list()
        # 二级数组
        groups = [a.tags for a in self.client.images.list()]
        for group in groups:
            for image in group:
                result.append(image)
        return result

    #
    def networks(self) -> list:
        """
        获取docker网络列表
        :return:
        """
        return [a.name for a in self.client.networks.list()]

    #
    def create_network(self, name: str):
        """
        创建docker网络
        :param name:
        :return:
        """
        if name not in self.networks():
            print(f"network:{name} --> creating")
            self.client.networks.create(name)
        else:
            print(f"network:{name} is exited --> pass")

    def continers(self, flag=False) -> list:
        """
        获取docker容器列表
        :param flag:
        :return:
        """
        return [a.name for a in self.client.containers.list(all=flag)]

    def volumes(self) -> list:
        """
        获取docker挂载列表
        :return:
        """
        return [a.name for a in self.client.volumes.list()]

    def pull_image(self, img_name: str):
        """
        拉取docker镜像
        :param img_name:
        :return:
        """
        if img_name not in self.images():
            print(f"---> pull image:{img_name}")
            self.client.images.pull(img_name)
        else:
            print(f"image:{img_name} is exited --> pass")

    def rm_image(self, img_name: str, force: bool):
        """
        移除镜像
        :param img_name:
        :param force:
        :return:
        """
        imgs = self.images()
        for _, img in enumerate(imgs):
            if img == img_name:
                img.remove(force=force)
                return
        print(f"image:{img_name} is not find ")

    def rm_container(self, name, force: bool):
        """
        移除容器
        :param name:
        :param force:
        :return:
        """
        cs = self.client.containers.list(all=True)
        for i, c in enumerate(cs):
            if c.name == name or c.short_id == name:
                print(f"find container:{c.name} --> remove it")
                c.remove(force=force)
                return
        print(f"container:{name} is not finded")

    def create_volume(self, name: str):
        """
        创建docker挂载
        :param name:挂载名称
        :return:
        """
        # create volume
        if name not in self.volumes():
            print(f"volume :{name} --> creating")
            self.client.volumes.create(name)
        else:
            print(f"volume:{name} is exited --> pass")

    # 创建并运行redis容器
    def run_redis_container(self, name, port, network, network_alias, volume, restart, img, password):
        """
        启动redis容器
        :param name: 名称
        :param port: 端口
        :param network: 使用docker网桥
        :param network_alias: 在docker局域网中的别名
        :param volume: 挂载映射
        :param restart: 重启策略
        :param img: 镜像源
        :param password: redis访问密码
        :return: 是否执行
        """
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                print(f"container:{name} is exist bud not run --> remove it")
                os.system(f"docker rm {name}")
            print(f"container{name} --> creating")
            cmd = f"docker run -itd -p {port} --name {name} --network {network} --network-alias {network_alias} -v {volume}:/data --restart={restart} {img} --requirepass {password} "
            print(f"CMD: {cmd}")
            os.system(cmd)
            return True
        else:
            print(f"container:{name} is exist and is running --> pass")
            return False

    # 创建并运行postgrest容器
    def run_pg_container(self, name, port, network, network_alias, volume, user, password, restart, img) -> bool:
        """
        启动postgres容器
        :param name:容器名
        :param port:端口
        :param network:网桥
        :param network_alias:网络别名
        :param volume:挂载映射
        :param user:postgres user
        :param password:postgres password
        :param restart:重启策略
        :param img:镜像源
        :return:是否执行
        """
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                os.system(f"docker rm {name}")
                print(f"container:{name} is exist and is stopped --> remove")
            print(f"container{name} --> creating")
            cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -v {volume}:/var/lib/postgresql/data -e POSTGRES_USER={user} -e POSTGRES_PASSWORD={password} -e ALLOW_IP_RANGE=0.0.0.0/0 --restart={restart} {img}"
            print(f"CMD: {cmd}")
            os.system(cmd)
            return True
        else:
            print(f"container:{name} is exist and is running --> pass")
            return False

    # 创建并运行mongodb容器
    def run_mongo_container(self, name, port, network, network_alias, volume, user, password, restart, img, cache,
                            memory,
                            memory_swap) -> bool:
        """
        运行mongodb 容器
        :param name: 容器名
        :param port: 端口
        :param network: docker网桥
        :param network_alias: ip别名
        :param volume: 挂载映射
        :param user: mongo user
        :param password:  mongo password
        :param restart: 重启策略
        :param img: 镜像源
        :param cache: mongo缓存大小
        :param memory: mongo最大占用内存(真实)
        :param memory_swap: mongo最大占用内存(虚拟)
        :return: 是否执行
        """
        if name not in self.continers(flag=False):
            if name in self.continers(True):
                os.system(f"docker rm {name}")
                print(f"container:{name} is exist and is stopped --> remove")
            print(f"container:{name} --> creating")
            cmd = f"docker run -itd --name {name} -p {port} --network {network} --network-alias {network_alias} -m {memory} --memory-swap {memory_swap} -e MONGO_INITDB_ROOT_USERNAME={user} -e MONGO_INITDB_ROOT_PASSWORD={password} -v {volume}:/data/db --restart={restart} {img} --wiredTigerCacheSizeGB {cache}"
            print(f"CMD: {cmd}")
            os.system(cmd)
            return True
        else:
            print(f"container:{name} is exist and is running --> pass")
            return False

    def info(self) -> dict:
        """
        获取当前容器列表基本信息
        :return:
        """
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
        """
        获取容器状态
        :param c_name:
        :return: restarting :-1、running:1 、paused:-1 、exited -1 no exist：0
        """
        cs = self.client.containers.list(all=True)
        for c in cs:
            if c.name == c_name and c.status == 'running':
                return 1
            if c.name == c_name and c.status != 'running':
                return -1
        return 0

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         a 
# Author:       yepeng
# Date:         2021/10/22 2:44 下午
# Description: 
# -------------------------------------------------------------------------------
import os
from typing import Union, List

# import docker
from docker import DockerClient, from_env
from docker.models.containers import Container


# noinspection PyBroadException
class DockerApi(object):
    """
    Docker Client Api
    """

    def __init__(self, client):
        self.client: DockerClient = client
        pass

    @classmethod
    def from_env(cls):
        c = from_env()
        return cls(c)

    # ------------Container----------------
    def test(self):
        c = self.client.containers.run('alpine', 'echo hello world')

    def run_container(self, image, name, network, volumes: Union[List[dict], None] = None,
                      ports: Union[dict, None] = None,
                      environment: Union[dict, None] = None, restart: Union[dict, None] = None,
                      commond=None) -> Union[Container, None]:
        # docker run -itd --name {name} -e NETWORK={network} -e ORIGIN={origin} -e INTERVAL={interval} -e NODE="{node}" -e WEBHOOK={webhook} --network {net} --network-alias {net_alias} --restart={restart} {img}'

        #               {'/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
        #                      '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}}
        #          environment (dict or list): Environment variables to set inside
        #                 the container, as a dictionary or a list of strings in the
        #                 format ``["SOMEVARIABLE=xxx"]``.

        # ``{"Name": "on-failure", "MaximumRetryCount": 5}``
        try:
            container = self.client.containers.run(image=image, detach=True, name=name, network=network,
                                                   volumes=volumes,
                                                   ports=ports,
                                                   environment=environment, restart_policy=restart,
                                                   command=commond)
            return container
        except Exception as e:
            print(f"ERROR:run container failed:{e}")
            return None

    def _all_container(self) -> List[Container]:
        return self.client.containers.list(all=True)

    def get_container(self, name_or_id) -> Union[Container, None]:
        for c in self._all_container():
            if c.name == name_or_id:
                return c
        return None

    def stop_container(self, name_or_id: str):
        for a in self._all_container():
            if a.name == name_or_id or a.short_id == name_or_id:
                a.stop()
                return True, "success"
        return False, "stop container failed,can not find it by name or short_id"

    def remove_container(self, name_or_id, force=True) -> (bool, str):
        for a in self._all_container():
            # print(f"{a.name} {a.status} {a.image.tags} {a.labels} {a.ports}")
            if a.name == name_or_id or a.short_id == name_or_id:
                if not force and a.status == 'running':
                    return False, "remove container failed,it is running ,but force = fasle"
                a.remove(force=force)
                return True, "success"
        return False, "remove container failed,can not find it by name or short_id"

    def continers(self, flag=False) -> list:
        """
        获取docker容器列表
        :param flag:
        :return:
        """
        return [a.name for a in self.client.containers.list(all=flag)]

    # ------------Image----------------
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

    def remove_image(self, img_name: str, force: bool):
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

    # ------------Network----------------
    def networks(self) -> list:
        """
        获取docker网络列表
        :return:
        """
        return [a.name for a in self.client.networks.list()]

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

    # ------------Volume----------------
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

    def volumes(self) -> list:
        """
        获取docker挂载列表
        :return:
        """
        return [a.name for a in self.client.volumes.list()]

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
            print(f"container:{name} --> creating")
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

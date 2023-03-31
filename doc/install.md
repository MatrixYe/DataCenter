#### 1 安装docker，如果已经安装，则跳过

```bash
#下载脚本
curl -fsSL https://get.docker.com -o get-docker.sh
#安装
sudo sh get-docker.sh
# 如果安装后提示没有权限，请添加docker到组
# 添加docker组
sudo groupadd docker
# 将当前用户添加到组docker
sudo gpasswd -a <用户名> docker
# 重启
sudo service docker restart
```

#### 2、安装conda，如果系统已经安装py3，跳过

```bash
#下载脚本
wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# 启动脚本
bash Miniconda3-latest-Linux-x86_64.sh 
#安装脚本安装后，重启shell即可
python --version
```

#### 3、执行初始化系统

这一步骤将下载py依赖及镜像,启动mongo数据库及redis数据库

```bash
cd DataCenter
```

```bash
make base
```

#### 4、构建引擎镜像

```shell
make build
```

注意，需要先构建基础镜像再构建其他镜像

```json
[
  {
    "name": "basic python image",
    "cmd": "docker build -t basic-py . -f imager/basic-py.Dockerfile",
    "desc": "自定义基础python镜像"
  },
  {
    "name": "Block Engine",
    "cmd": "docker build -t sync-block . -f imager/sync_block.Dockerfile",
    "desc": "区块高度同步器基础镜像"
  },
  {
    "name": "Event Engine",
    "cmd": "docker build -t sync-event . -f imager/sync_event.Dockerfile",
    "desc": "通用事件同步器基础镜像"
  },
  {
    "name": "Oracle Engine",
    "cmd": "docker build -t sync-oracle . -f imager/sync_oracle.Dockerfile",
    "desc": "喂价源同步器基础镜像"
  },
  {
    "name": "Rpc Server",
    "cmd": "docker build -t server-rpc . -f imager/server_rpc.Dockerfile",
    "desc": "RPC-server服务镜像"
  },
  {
    "name": "Http server",
    "cmd": "docker build -t server-http . -f imager/server_http.Dockerfile",
    "desc": "Http-server服务镜像"
  }
]
```

#### 启动RPC服务和HTTP服务

```shell
make start
```

#### 启动服务后，执行任务

根据自定义脚本运行


FROM python:3.10
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt && pip install -e . && python --version

# 区块网络名称
ENV NETWORK=""
# 同步起始点
ENV ORIGIN=0
# 同步时间间隔
ENV INTERVAL=0
# 数据服务商节点
ENV NODE=""
# 消息推送url
ENV WEBHOOK=""

#启动main
ENTRYPOINT ["sh","-c","python main_block.py --network $NETWORK --origin $ORIGIN --interval $INTERVAL --node $NODE --webhook $WEBHOOK"]

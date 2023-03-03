FROM basic-py:latest
WORKDIR /app
ADD . .
RUN pip install -e .


# 区块网络
ENV NETWORK=""
# 喂价源提供商(例如chainlink)
ENV PROVIDER=""
# 喂价源地址
ENV TARGET=""
# 历史同步数量(对于uni是区块数，对于chainlink是answer数量)
ENV HISTORY=0
# 数据服务商节点
ENV NODE=""
# 消息推送地址
ENV WEBHOOK=""

#启动main
ENTRYPOINT ["sh","-c","python main_oracle.py --network $NETWORK --provider $PROVIDER --target $TARGET --history $HISTORY --node $NODE --webhook $WEBHOOK"]

FROM python:3.10
WORKDIR /app
ADD . .
RUN python --version  \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install -r requirements.txt  \
    && pip install -e .

# 区块网络名称
ENV NETWORK=""
# event out 合约地址
ENV TARGET=""
# 同步起始点
ENV ORIGIN=0
# 数据服务商节点
ENV NODE=""
# 同步延时(区块)
ENV DELAY=0
# 追逐模式下最大同步区块间隔
ENV RANGE=1000
# 消息推送地址
ENV WEBHOOK=""

#启动main
ENTRYPOINT ["sh","-c","python main_event.py --network $NETWORK --target $TARGET --origin $ORIGIN --node $NODE --delay $DELAY --range $RANGE --webhook $WEBHOOK"]

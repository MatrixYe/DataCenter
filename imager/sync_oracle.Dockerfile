FROM python:3.10
WORKDIR /app
ADD . .
RUN python --version  \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install -r requirements.txt  \
    && pip install -e .

# 传递参数
ENV NETWORK=""
ENV ORIGIN=0
ENV RELOAD=False
ENV NODE=""
ENV INTERVAL=0

#运行python的命令
ENTRYPOINT ["sh","-c","python cmd/main_block.py --network $NETWORK --origin $ORIGIN --interval $INTERVAL --reload $RELOAD --node $NODE"]

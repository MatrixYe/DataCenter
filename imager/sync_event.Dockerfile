FROM python:3.10
WORKDIR /app
ADD . .
RUN python --version  \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install -r requirements.txt  \
    && pip install -e .

# 传递参数
ENV NETWORK=""
ENV TARGET=""
ENV ORIGIN=0
ENV NODE=""
ENV DELAY=0
ENV RANGE=1000
ENV RELOAD=False

#运行python的命令
ENTRYPOINT ["sh","-c","python main_event.py --network $NETWORK --target $TARGET --origin $ORIGIN --node $NODE --delay $DELAY --range $RANGE --reload $RELOAD"]

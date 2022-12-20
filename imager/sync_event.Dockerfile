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
ENV RELOAD=False

#运行python的命令
ENTRYPOINT ["sh","-c","python cmd/main_event.py --network $NETWORK --origin $TARGET --reload $ORIGIN --node $NODE --target $RELOAD"]

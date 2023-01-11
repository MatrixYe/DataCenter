FROM python:3.10
WORKDIR /app
ADD . .
RUN python --version  \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install -r requirements.txt  \
    && pip install -e .
#        "network": args.network.lower(),
 #        "provider": args.provider,
 #        "target": args.target,
 #        "history": args.history,
 #        "node": args.node,
 #        "webhook": args.webhook,
# 传递参数
ENV NETWORK=""
ENV PROVIDER=""
ENV TARGET=""
ENV HISTORY=0
ENV NODE=""
ENV WEBHOOK=""

#运行python的命令
ENTRYPOINT ["sh","-c","python main_oracle.py --network $NETWORK --provider $PROVIDER --target $TARGET --history $HISTORY --node $NODE --webhook $WEBHOOK"]

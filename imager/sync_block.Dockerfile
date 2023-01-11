FROM python:3.10
WORKDIR /app
ADD . .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install -r requirements.txt && pip install -e . && python --version

# 传递参数
ENV NETWORK=""
ENV ORIGIN=0
ENV INTERVAL=0
ENV NODE=""
ENV WEBHOOK=""

#运行python的命令
ENTRYPOINT ["sh","-c","python main_block.py --network $NETWORK --origin $ORIGIN --interval $INTERVAL --node $NODE --webhook $WEBHOOK"]

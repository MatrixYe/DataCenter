FROM python:3.10
WORKDIR /app
ADD . .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install -r requirements.txt && pip install -e . && python --version

# 传递参数
ENV HOST="0.0.0.0"
ENV PORT=9005

EXPOSE 9005

#运行python的命令
ENTRYPOINT ["sh","-c","python main_server.py --host $HOST --port $PORT"]

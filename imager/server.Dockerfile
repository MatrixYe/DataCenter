FROM python:3.10
WORKDIR /app
ADD . .
#RUN pip install -r requirements.txt && pip install -e . && python --version
RUN pip install -r requirements.txt && pip install -e . && python --version

# RPC服务地址
ENV HOST="0.0.0.0"
# RPC服务对内端口
ENV PORT=9005
# RPC服务对外端口
EXPOSE 9005

#启动main
ENTRYPOINT ["sh","-c","python main_server.py --host $HOST --port $PORT"]

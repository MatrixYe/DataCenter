FROM python:3.10
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt && pip install -e . && python --version

# RPC服务地址
ENV HOST="0.0.0.0"
# RPC服务对内端口
ENV PORT=9006
# RPC服务对外端口
EXPOSE 9006

#启动main
#ENTRYPOINT ["uvicorn","main_https:app","--host","0.0.0.0","--port","9006"]
#ENTRYPOINT ["sh","-c","uvicorn main_https:app --host $HOST --port $PORT"]
ENTRYPOINT ["sh","-c","python main_https.py --host $HOST --port $PORT"]


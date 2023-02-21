FROM python:3.10
WORKDIR /app
ADD . .
#RUN pip install -r requirements.txt && pip install -e . && python --version
RUN pip install -r requirements.txt && pip install -e . && python --version

# RPC服务地址
ENV HOST="0.0.0.0"
# RPC服务对内端口
ENV PORT=8000
# RPC服务对外端口
EXPOSE 8000

#启动main
ENTRYPOINT ["uvicorn","main_webs:app","--host","0.0.0.0","--port","8000"]

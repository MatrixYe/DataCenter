#拉取docker环境
FROM python

#设置工作目录
WORKDIR /app

#将dockerfile同级目录的文件传到docker容器内的app文件夹下
ADD . .
RUN pip install -r  requirements.txt

# 传递参数
ENV TARGET=""
ENV RPC=""


#运行python的命令
CMD ["python","main.py --target $TARGET --rpc $RPC"]

#拉取docker环境
FROM conda/miniconda3:latest


#设置工作目录
WORKDIR /app

#将dockerfile同级目录的文件传到docker容器内的app文件夹下
ADD . .
RUN python --version && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install -r requirements.txt && pip install -e .

# 传递参数
ENV TARGET="FUCK"
ENV NODE="YOU"

#运行python的命令
ENTRYPOINT ["sh","-c","python engine/test.py --target $TARGET --node $NODE"]
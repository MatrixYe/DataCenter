.PHONY: base clear build stop server destroy help
IMAGE = imager
## 初始化系统
base:
	pip install -r requirements.txt
	python base.py

## 清除冗余镜像、容器等
clear:
	docker system prune

## 构建引擎基础镜像
build:
	echo "hello ,this is build"
	python build.py

## 启动rpc服务
start-server:
	echo "hello,this is server,run it"
	docker rm -f server
	docker run -itd --name server -p 9005:9005 --network net_center -e HOST="0.0.0.0" -e PORT=9005 -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker server

## 停止server
stop-server:
	echo "hello,this is server,stop it"
	docker rm -f server

## 生成grpc py file
gen-rpc:
	cd pb && python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. ./server.proto

## 生成grpc doc文件
gen-doc:
	docker run --rm -v $(pwd)/doc:/out -v $(pwd)/pb:/protos pseudomuto/protoc-gen-doc

## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo ' make target'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	helpMessage = match(lastLine, /^## (.*)/); \
	if (helpMessage) { \
	helpCommand = substr($$1, 0, index($$1, ":")-1); \
	helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
	printf " %-20s %s\n", helpCommand, helpMessage; \
	} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

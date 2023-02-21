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
## 启动相关服务容器
start:
	python start.py

## 生成grpc py file
gen-rpc:
	cd pb && python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. ./server.proto

## 生成grpc doc文件
gen-doc:
	docker run --rm -v $(PWD)/doc:/out -v $(PWD)/pb:/protos pseudomuto/protoc-gen-doc

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

.PHONY: base product build start stop clear gengo conf start-listen stop_listen help
IMAGE = imager

base:
	echo "hello,this is base"

build:
	echo "hello ,this is build"

server:
	echo "hello,this is server"

test-build:
	docker build -t test . -f $(IMAGE)/test.Dockerfile

test-start:
	docker rm -f test &&  docker run -itd --name test -e TARGET="0x1312312312312312" -e RPC="https://infura.com" test && docker logs -f test


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
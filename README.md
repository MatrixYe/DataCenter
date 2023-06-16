# 数据中心

## 安装文档

[install.md](doc/install.md)

## 使用方法

```go
func main() {
	// 连接core
	conn, err := grpc.Dial("localhost:9005", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	// 构建grpc客户端
	client := pb.NewDataCenterClient(conn)
	//请求数据
	reply, err := client.EventFilter(context.Background(), &pb.EventFilterAsk{
		Network: "arbitrum_goerli",
		Target:  "0x59df7f24187973453b1bc01244143ca18b6059c4",
		Start:   25929050,
		End:     25929090,
		Senders: nil,
		Desc:    false,
	})
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Println(len(reply.Events))
	for i, event := range reply.Events {
		fmt.Printf("[%d]发现event: block=%d index=%d txhash=%s\n", i, event.BlockNumber, event.Index, event.TxHash)
	}
}

```
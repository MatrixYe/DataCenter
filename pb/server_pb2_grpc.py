# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import server_pb2 as server__pb2


class DataCenterStub(object):
    """*
    Service for handling data center.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BlockLast = channel.unary_unary(
            '/pb.DataCenter/BlockLast',
            request_serializer=server__pb2.BlockLastAsk.SerializeToString,
            response_deserializer=server__pb2.BlockLastReply.FromString,
        )
        self.BlockDetail = channel.unary_unary(
            '/pb.DataCenter/BlockDetail',
            request_serializer=server__pb2.BlockDetailAsk.SerializeToString,
            response_deserializer=server__pb2.BlockDetailReply.FromString,
        )
        self.EventLast = channel.unary_unary(
            '/pb.DataCenter/EventLast',
            request_serializer=server__pb2.EventLastAsk.SerializeToString,
            response_deserializer=server__pb2.EventLastReply.FromString,
        )
        self.EventFilter = channel.unary_unary(
            '/pb.DataCenter/EventFilter',
            request_serializer=server__pb2.EventFilterAsk.SerializeToString,
            response_deserializer=server__pb2.EventFilterReply.FromString,
        )
        self.OraclePrice = channel.unary_unary(
            '/pb.DataCenter/OraclePrice',
            request_serializer=server__pb2.OraclePriceAsk.SerializeToString,
            response_deserializer=server__pb2.OraclePriceReply.FromString,
        )
        self.OraclePriceChg = channel.unary_unary(
            '/pb.DataCenter/OraclePriceChg',
            request_serializer=server__pb2.OraclePriceChgAsk.SerializeToString,
            response_deserializer=server__pb2.OraclePriceChgReply.FromString,
        )
        self.OracleData = channel.unary_unary(
            '/pb.DataCenter/OracleData',
            request_serializer=server__pb2.OracleDataAsk.SerializeToString,
            response_deserializer=server__pb2.OracleDataReply.FromString,
        )
        self.StartSyncBlock = channel.unary_unary(
            '/pb.DataCenter/StartSyncBlock',
            request_serializer=server__pb2.StartSyncBlockAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )
        self.StopSyncBlock = channel.unary_unary(
            '/pb.DataCenter/StopSyncBlock',
            request_serializer=server__pb2.StopSyncBlockAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )
        self.StartSyncEvent = channel.unary_unary(
            '/pb.DataCenter/StartSyncEvent',
            request_serializer=server__pb2.StartSyncEventAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )
        self.StopSyncEvent = channel.unary_unary(
            '/pb.DataCenter/StopSyncEvent',
            request_serializer=server__pb2.StopSyncEventAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )
        self.StartSyncOracle = channel.unary_unary(
            '/pb.DataCenter/StartSyncOracle',
            request_serializer=server__pb2.StartSyncOracleAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )
        self.StopSyncOracle = channel.unary_unary(
            '/pb.DataCenter/StopSyncOracle',
            request_serializer=server__pb2.StopSyncOracleAsk.SerializeToString,
            response_deserializer=server__pb2.ComReply.FromString,
        )


class DataCenterServicer(object):
    """*
    Service for handling data center.
    """

    def BlockLast(self, request, context):
        """获取最新block 高度
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BlockDetail(self, request, context):
        """获取指定高度block详情
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EventLast(self, request, context):
        """获取event out 最新同步高度
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EventFilter(self, request, context):
        """获取event 事件列表
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OraclePrice(self, request, context):
        """获取喂价源最新价格
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OraclePriceChg(self, request, context):
        """获取喂价源价格变化率
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OracleData(self, request, context):
        """获取喂价源价格变动数据集合(K线处理由其他服务完成，此处不处理)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartSyncBlock(self, request, context):
        """新增同步一条block数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopSyncBlock(self, request, context):
        """停止同步一条block数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartSyncEvent(self, request, context):
        """新增同步一条event out数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopSyncEvent(self, request, context):
        """停止同步一条event out数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartSyncOracle(self, request, context):
        """新增同步一条oracle数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopSyncOracle(self, request, context):
        """停止同步一条oracle数据
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataCenterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'BlockLast': grpc.unary_unary_rpc_method_handler(
            servicer.BlockLast,
            request_deserializer=server__pb2.BlockLastAsk.FromString,
            response_serializer=server__pb2.BlockLastReply.SerializeToString,
        ),
        'BlockDetail': grpc.unary_unary_rpc_method_handler(
            servicer.BlockDetail,
            request_deserializer=server__pb2.BlockDetailAsk.FromString,
            response_serializer=server__pb2.BlockDetailReply.SerializeToString,
        ),
        'EventLast': grpc.unary_unary_rpc_method_handler(
            servicer.EventLast,
            request_deserializer=server__pb2.EventLastAsk.FromString,
            response_serializer=server__pb2.EventLastReply.SerializeToString,
        ),
        'EventFilter': grpc.unary_unary_rpc_method_handler(
            servicer.EventFilter,
            request_deserializer=server__pb2.EventFilterAsk.FromString,
            response_serializer=server__pb2.EventFilterReply.SerializeToString,
        ),
        'OraclePrice': grpc.unary_unary_rpc_method_handler(
            servicer.OraclePrice,
            request_deserializer=server__pb2.OraclePriceAsk.FromString,
            response_serializer=server__pb2.OraclePriceReply.SerializeToString,
        ),
        'OraclePriceChg': grpc.unary_unary_rpc_method_handler(
            servicer.OraclePriceChg,
            request_deserializer=server__pb2.OraclePriceChgAsk.FromString,
            response_serializer=server__pb2.OraclePriceChgReply.SerializeToString,
        ),
        'OracleData': grpc.unary_unary_rpc_method_handler(
            servicer.OracleData,
            request_deserializer=server__pb2.OracleDataAsk.FromString,
            response_serializer=server__pb2.OracleDataReply.SerializeToString,
        ),
        'StartSyncBlock': grpc.unary_unary_rpc_method_handler(
            servicer.StartSyncBlock,
            request_deserializer=server__pb2.StartSyncBlockAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
        'StopSyncBlock': grpc.unary_unary_rpc_method_handler(
            servicer.StopSyncBlock,
            request_deserializer=server__pb2.StopSyncBlockAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
        'StartSyncEvent': grpc.unary_unary_rpc_method_handler(
            servicer.StartSyncEvent,
            request_deserializer=server__pb2.StartSyncEventAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
        'StopSyncEvent': grpc.unary_unary_rpc_method_handler(
            servicer.StopSyncEvent,
            request_deserializer=server__pb2.StopSyncEventAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
        'StartSyncOracle': grpc.unary_unary_rpc_method_handler(
            servicer.StartSyncOracle,
            request_deserializer=server__pb2.StartSyncOracleAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
        'StopSyncOracle': grpc.unary_unary_rpc_method_handler(
            servicer.StopSyncOracle,
            request_deserializer=server__pb2.StopSyncOracleAsk.FromString,
            response_serializer=server__pb2.ComReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'pb.DataCenter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class DataCenter(object):
    """*
    Service for handling data center.
    """

    @staticmethod
    def BlockLast(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/BlockLast',
                                             server__pb2.BlockLastAsk.SerializeToString,
                                             server__pb2.BlockLastReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BlockDetail(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/BlockDetail',
                                             server__pb2.BlockDetailAsk.SerializeToString,
                                             server__pb2.BlockDetailReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EventLast(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/EventLast',
                                             server__pb2.EventLastAsk.SerializeToString,
                                             server__pb2.EventLastReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EventFilter(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/EventFilter',
                                             server__pb2.EventFilterAsk.SerializeToString,
                                             server__pb2.EventFilterReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OraclePrice(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/OraclePrice',
                                             server__pb2.OraclePriceAsk.SerializeToString,
                                             server__pb2.OraclePriceReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OraclePriceChg(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/OraclePriceChg',
                                             server__pb2.OraclePriceChgAsk.SerializeToString,
                                             server__pb2.OraclePriceChgReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OracleData(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/OracleData',
                                             server__pb2.OracleDataAsk.SerializeToString,
                                             server__pb2.OracleDataReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartSyncBlock(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StartSyncBlock',
                                             server__pb2.StartSyncBlockAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopSyncBlock(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StopSyncBlock',
                                             server__pb2.StopSyncBlockAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartSyncEvent(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StartSyncEvent',
                                             server__pb2.StartSyncEventAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopSyncEvent(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StopSyncEvent',
                                             server__pb2.StopSyncEventAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartSyncOracle(request,
                        target,
                        options=(),
                        channel_credentials=None,
                        call_credentials=None,
                        insecure=False,
                        compression=None,
                        wait_for_ready=None,
                        timeout=None,
                        metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StartSyncOracle',
                                             server__pb2.StartSyncOracleAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopSyncOracle(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb.DataCenter/StopSyncOracle',
                                             server__pb2.StopSyncOracleAsk.SerializeToString,
                                             server__pb2.ComReply.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

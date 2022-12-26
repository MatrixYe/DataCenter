# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cserver.proto\x12\x02pb\"\x1f\n\x0c\x42lockLastAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\"R\n\x0e\x42lockLastReply\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06height\x18\x02 \x01(\x04\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x0c\n\x04hash\x18\x04 \x01(\t\"1\n\x0e\x42lockDetailAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06height\x18\x02 \x01(\x04\"T\n\x10\x42lockDetailReply\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06height\x18\x02 \x01(\x04\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x0c\n\x04hash\x18\x04 \x01(\t\"/\n\x0c\x45ventLastAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\" \n\x0e\x45ventLastReply\x12\x0e\n\x06height\x18\x02 \x01(\x04\"n\n\x0e\x45ventFilterAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\r\n\x05start\x18\x03 \x01(\x04\x12\x0b\n\x03\x65nd\x18\x04 \x01(\x04\x12\x0f\n\x07senders\x18\x05 \x03(\t\x12\x0e\n\x06itypes\x18\x06 \x03(\x05\"\xaa\x01\n\x10\x45ventFilterReply\x12-\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x1d.pb.EventFilterReply.RawEvent\x1ag\n\x08RawEvent\x12\x0e\n\x06sender\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\r\x12\r\n\x05value\x18\x05 \x01(\x0c\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\r\n\x05index\x18\x02 \x01(\x04\x12\x0f\n\x07tx_hash\x18\x06 \x01(\t\"T\n\x0eOraclePriceAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x10\n\x08\x64\x65\x61\x64line\x18\x03 \x01(\x04\x12\x0f\n\x07reverse\x18\x04 \x01(\x08\"i\n\x10OraclePriceReply\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x02\x12\x11\n\ttimestamp\x18\x04 \x01(\x04\x12\x12\n\nis_reverse\x18\x05 \x01(\x08\"a\n\x11OraclePriceChgAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\r\n\x05start\x18\x03 \x01(\x04\x12\x0b\n\x03\x65nd\x18\x04 \x01(\x04\x12\x0f\n\x07reverse\x18\x05 \x01(\x08\"W\n\x13OraclePriceChgReply\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x0b\n\x03\x63hg\x18\x03 \x01(\x02\x12\x12\n\nis_reverse\x18\x04 \x01(\x08\"m\n\x0eOracleKlineAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\r\n\x05level\x18\x03 \x01(\x04\x12\r\n\x05start\x18\x04 \x01(\x04\x12\x0b\n\x03\x65nd\x18\x05 \x01(\x04\x12\x0f\n\x07reverse\x18\x06 \x01(\x08\"\xfd\x01\n\x10OracleKlineReply\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05level\x18\x04 \x01(\r\x12\r\n\x05start\x18\x05 \x01(\x04\x12\x0b\n\x03\x65nd\x18\x06 \x01(\x04\x12\x0c\n\x04pair\x18\x07 \x01(\t\x12,\n\x07\x63\x61ndles\x18\x08 \x03(\x0b\x32\x1b.pb.OracleKlineReply.Candle\x1aS\n\x06\x43\x61ndle\x12\x0c\n\x04open\x18\x01 \x01(\t\x12\r\n\x05\x63lose\x18\x02 \x01(\x02\x12\x0c\n\x04high\x18\x03 \x01(\x02\x12\x0b\n\x03low\x18\x04 \x01(\x02\x12\x11\n\ttimestamp\x18\x05 \x01(\x04\"d\n\x11StartSyncBlockAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06origin\x18\x02 \x01(\x04\x12\x10\n\x08interval\x18\x03 \x01(\r\x12\x0c\n\x04node\x18\x04 \x01(\t\x12\x0e\n\x06reload\x18\x05 \x01(\x08\"#\n\x10StopSyncBlockAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\"\x80\x01\n\x11StartSyncEventAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x0e\n\x06origin\x18\x03 \x01(\x04\x12\x0c\n\x04node\x18\x04 \x01(\t\x12\r\n\x05\x64\x65lay\x18\x05 \x01(\r\x12\r\n\x05range\x18\x06 \x01(\r\x12\x0e\n\x06reload\x18\x07 \x01(\x08\"3\n\x10StopSyncEventAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"c\n\x12StartSyncOracleAsk\x12\x0f\n\x07netwrok\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x0e\n\x06origin\x18\x03 \x01(\x04\x12\x0c\n\x04node\x18\x04 \x01(\t\x12\x0e\n\x06reload\x18\x05 \x01(\x08\"4\n\x11StopSyncOracleAsk\x12\x0f\n\x07network\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\":\n\x08\x43omReply\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08short_id\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t2\xe0\x05\n\nDataCenter\x12\x31\n\tBlockLast\x12\x10.pb.BlockLastAsk\x1a\x12.pb.BlockLastReply\x12\x37\n\x0b\x42lockDetail\x12\x12.pb.BlockDetailAsk\x1a\x14.pb.BlockDetailReply\x12\x31\n\tEventLast\x12\x10.pb.EventLastAsk\x1a\x12.pb.EventLastReply\x12\x37\n\x0b\x45ventFilter\x12\x12.pb.EventFilterAsk\x1a\x14.pb.EventFilterReply\x12\x37\n\x0bOraclePrice\x12\x12.pb.OraclePriceAsk\x1a\x14.pb.OraclePriceReply\x12@\n\x0eOraclePriceChg\x12\x15.pb.OraclePriceChgAsk\x1a\x17.pb.OraclePriceChgReply\x12\x37\n\x0bOracleKline\x12\x12.pb.OracleKlineAsk\x1a\x14.pb.OracleKlineReply\x12\x35\n\x0eStartSyncBlock\x12\x15.pb.StartSyncBlockAsk\x1a\x0c.pb.ComReply\x12\x33\n\rStopSyncBlock\x12\x14.pb.StopSyncBlockAsk\x1a\x0c.pb.ComReply\x12\x35\n\x0eStartSyncEvent\x12\x15.pb.StartSyncEventAsk\x1a\x0c.pb.ComReply\x12\x33\n\rStopSyncEvent\x12\x14.pb.StopSyncEventAsk\x1a\x0c.pb.ComReply\x12\x37\n\x0fStartSyncOracle\x12\x16.pb.StartSyncOracleAsk\x1a\x0c.pb.ComReply\x12\x35\n\x0eStopSyncOracle\x12\x15.pb.StopSyncOracleAsk\x1a\x0c.pb.ComReplyB\x07Z\x05./;pbb\x06proto3')

_BLOCKLASTASK = DESCRIPTOR.message_types_by_name['BlockLastAsk']
_BLOCKLASTREPLY = DESCRIPTOR.message_types_by_name['BlockLastReply']
_BLOCKDETAILASK = DESCRIPTOR.message_types_by_name['BlockDetailAsk']
_BLOCKDETAILREPLY = DESCRIPTOR.message_types_by_name['BlockDetailReply']
_EVENTLASTASK = DESCRIPTOR.message_types_by_name['EventLastAsk']
_EVENTLASTREPLY = DESCRIPTOR.message_types_by_name['EventLastReply']
_EVENTFILTERASK = DESCRIPTOR.message_types_by_name['EventFilterAsk']
_EVENTFILTERREPLY = DESCRIPTOR.message_types_by_name['EventFilterReply']
_EVENTFILTERREPLY_RAWEVENT = _EVENTFILTERREPLY.nested_types_by_name['RawEvent']
_ORACLEPRICEASK = DESCRIPTOR.message_types_by_name['OraclePriceAsk']
_ORACLEPRICEREPLY = DESCRIPTOR.message_types_by_name['OraclePriceReply']
_ORACLEPRICECHGASK = DESCRIPTOR.message_types_by_name['OraclePriceChgAsk']
_ORACLEPRICECHGREPLY = DESCRIPTOR.message_types_by_name['OraclePriceChgReply']
_ORACLEKLINEASK = DESCRIPTOR.message_types_by_name['OracleKlineAsk']
_ORACLEKLINEREPLY = DESCRIPTOR.message_types_by_name['OracleKlineReply']
_ORACLEKLINEREPLY_CANDLE = _ORACLEKLINEREPLY.nested_types_by_name['Candle']
_STARTSYNCBLOCKASK = DESCRIPTOR.message_types_by_name['StartSyncBlockAsk']
_STOPSYNCBLOCKASK = DESCRIPTOR.message_types_by_name['StopSyncBlockAsk']
_STARTSYNCEVENTASK = DESCRIPTOR.message_types_by_name['StartSyncEventAsk']
_STOPSYNCEVENTASK = DESCRIPTOR.message_types_by_name['StopSyncEventAsk']
_STARTSYNCORACLEASK = DESCRIPTOR.message_types_by_name['StartSyncOracleAsk']
_STOPSYNCORACLEASK = DESCRIPTOR.message_types_by_name['StopSyncOracleAsk']
_COMREPLY = DESCRIPTOR.message_types_by_name['ComReply']
BlockLastAsk = _reflection.GeneratedProtocolMessageType('BlockLastAsk', (_message.Message,), {
    'DESCRIPTOR': _BLOCKLASTASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.BlockLastAsk)
})
_sym_db.RegisterMessage(BlockLastAsk)

BlockLastReply = _reflection.GeneratedProtocolMessageType('BlockLastReply', (_message.Message,), {
    'DESCRIPTOR': _BLOCKLASTREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.BlockLastReply)
})
_sym_db.RegisterMessage(BlockLastReply)

BlockDetailAsk = _reflection.GeneratedProtocolMessageType('BlockDetailAsk', (_message.Message,), {
    'DESCRIPTOR': _BLOCKDETAILASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.BlockDetailAsk)
})
_sym_db.RegisterMessage(BlockDetailAsk)

BlockDetailReply = _reflection.GeneratedProtocolMessageType('BlockDetailReply', (_message.Message,), {
    'DESCRIPTOR': _BLOCKDETAILREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.BlockDetailReply)
})
_sym_db.RegisterMessage(BlockDetailReply)

EventLastAsk = _reflection.GeneratedProtocolMessageType('EventLastAsk', (_message.Message,), {
    'DESCRIPTOR': _EVENTLASTASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.EventLastAsk)
})
_sym_db.RegisterMessage(EventLastAsk)

EventLastReply = _reflection.GeneratedProtocolMessageType('EventLastReply', (_message.Message,), {
    'DESCRIPTOR': _EVENTLASTREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.EventLastReply)
})
_sym_db.RegisterMessage(EventLastReply)

EventFilterAsk = _reflection.GeneratedProtocolMessageType('EventFilterAsk', (_message.Message,), {
    'DESCRIPTOR': _EVENTFILTERASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.EventFilterAsk)
})
_sym_db.RegisterMessage(EventFilterAsk)

EventFilterReply = _reflection.GeneratedProtocolMessageType('EventFilterReply', (_message.Message,), {

    'RawEvent': _reflection.GeneratedProtocolMessageType('RawEvent', (_message.Message,), {
        'DESCRIPTOR': _EVENTFILTERREPLY_RAWEVENT,
        '__module__': 'server_pb2'
        # @@protoc_insertion_point(class_scope:pb.EventFilterReply.RawEvent)
    })
    ,
    'DESCRIPTOR': _EVENTFILTERREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.EventFilterReply)
})
_sym_db.RegisterMessage(EventFilterReply)
_sym_db.RegisterMessage(EventFilterReply.RawEvent)

OraclePriceAsk = _reflection.GeneratedProtocolMessageType('OraclePriceAsk', (_message.Message,), {
    'DESCRIPTOR': _ORACLEPRICEASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OraclePriceAsk)
})
_sym_db.RegisterMessage(OraclePriceAsk)

OraclePriceReply = _reflection.GeneratedProtocolMessageType('OraclePriceReply', (_message.Message,), {
    'DESCRIPTOR': _ORACLEPRICEREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OraclePriceReply)
})
_sym_db.RegisterMessage(OraclePriceReply)

OraclePriceChgAsk = _reflection.GeneratedProtocolMessageType('OraclePriceChgAsk', (_message.Message,), {
    'DESCRIPTOR': _ORACLEPRICECHGASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OraclePriceChgAsk)
})
_sym_db.RegisterMessage(OraclePriceChgAsk)

OraclePriceChgReply = _reflection.GeneratedProtocolMessageType('OraclePriceChgReply', (_message.Message,), {
    'DESCRIPTOR': _ORACLEPRICECHGREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OraclePriceChgReply)
})
_sym_db.RegisterMessage(OraclePriceChgReply)

OracleKlineAsk = _reflection.GeneratedProtocolMessageType('OracleKlineAsk', (_message.Message,), {
    'DESCRIPTOR': _ORACLEKLINEASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OracleKlineAsk)
})
_sym_db.RegisterMessage(OracleKlineAsk)

OracleKlineReply = _reflection.GeneratedProtocolMessageType('OracleKlineReply', (_message.Message,), {

    'Candle': _reflection.GeneratedProtocolMessageType('Candle', (_message.Message,), {
        'DESCRIPTOR': _ORACLEKLINEREPLY_CANDLE,
        '__module__': 'server_pb2'
        # @@protoc_insertion_point(class_scope:pb.OracleKlineReply.Candle)
    })
    ,
    'DESCRIPTOR': _ORACLEKLINEREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.OracleKlineReply)
})
_sym_db.RegisterMessage(OracleKlineReply)
_sym_db.RegisterMessage(OracleKlineReply.Candle)

StartSyncBlockAsk = _reflection.GeneratedProtocolMessageType('StartSyncBlockAsk', (_message.Message,), {
    'DESCRIPTOR': _STARTSYNCBLOCKASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StartSyncBlockAsk)
})
_sym_db.RegisterMessage(StartSyncBlockAsk)

StopSyncBlockAsk = _reflection.GeneratedProtocolMessageType('StopSyncBlockAsk', (_message.Message,), {
    'DESCRIPTOR': _STOPSYNCBLOCKASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StopSyncBlockAsk)
})
_sym_db.RegisterMessage(StopSyncBlockAsk)

StartSyncEventAsk = _reflection.GeneratedProtocolMessageType('StartSyncEventAsk', (_message.Message,), {
    'DESCRIPTOR': _STARTSYNCEVENTASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StartSyncEventAsk)
})
_sym_db.RegisterMessage(StartSyncEventAsk)

StopSyncEventAsk = _reflection.GeneratedProtocolMessageType('StopSyncEventAsk', (_message.Message,), {
    'DESCRIPTOR': _STOPSYNCEVENTASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StopSyncEventAsk)
})
_sym_db.RegisterMessage(StopSyncEventAsk)

StartSyncOracleAsk = _reflection.GeneratedProtocolMessageType('StartSyncOracleAsk', (_message.Message,), {
    'DESCRIPTOR': _STARTSYNCORACLEASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StartSyncOracleAsk)
})
_sym_db.RegisterMessage(StartSyncOracleAsk)

StopSyncOracleAsk = _reflection.GeneratedProtocolMessageType('StopSyncOracleAsk', (_message.Message,), {
    'DESCRIPTOR': _STOPSYNCORACLEASK,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.StopSyncOracleAsk)
})
_sym_db.RegisterMessage(StopSyncOracleAsk)

ComReply = _reflection.GeneratedProtocolMessageType('ComReply', (_message.Message,), {
    'DESCRIPTOR': _COMREPLY,
    '__module__': 'server_pb2'
    # @@protoc_insertion_point(class_scope:pb.ComReply)
})
_sym_db.RegisterMessage(ComReply)

_DATACENTER = DESCRIPTOR.services_by_name['DataCenter']
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z\005./;pb'
    _BLOCKLASTASK._serialized_start = 20
    _BLOCKLASTASK._serialized_end = 51
    _BLOCKLASTREPLY._serialized_start = 53
    _BLOCKLASTREPLY._serialized_end = 135
    _BLOCKDETAILASK._serialized_start = 137
    _BLOCKDETAILASK._serialized_end = 186
    _BLOCKDETAILREPLY._serialized_start = 188
    _BLOCKDETAILREPLY._serialized_end = 272
    _EVENTLASTASK._serialized_start = 274
    _EVENTLASTASK._serialized_end = 321
    _EVENTLASTREPLY._serialized_start = 323
    _EVENTLASTREPLY._serialized_end = 355
    _EVENTFILTERASK._serialized_start = 357
    _EVENTFILTERASK._serialized_end = 467
    _EVENTFILTERREPLY._serialized_start = 470
    _EVENTFILTERREPLY._serialized_end = 640
    _EVENTFILTERREPLY_RAWEVENT._serialized_start = 537
    _EVENTFILTERREPLY_RAWEVENT._serialized_end = 640
    _ORACLEPRICEASK._serialized_start = 642
    _ORACLEPRICEASK._serialized_end = 726
    _ORACLEPRICEREPLY._serialized_start = 728
    _ORACLEPRICEREPLY._serialized_end = 833
    _ORACLEPRICECHGASK._serialized_start = 835
    _ORACLEPRICECHGASK._serialized_end = 932
    _ORACLEPRICECHGREPLY._serialized_start = 934
    _ORACLEPRICECHGREPLY._serialized_end = 1021
    _ORACLEKLINEASK._serialized_start = 1023
    _ORACLEKLINEASK._serialized_end = 1132
    _ORACLEKLINEREPLY._serialized_start = 1135
    _ORACLEKLINEREPLY._serialized_end = 1388
    _ORACLEKLINEREPLY_CANDLE._serialized_start = 1305
    _ORACLEKLINEREPLY_CANDLE._serialized_end = 1388
    _STARTSYNCBLOCKASK._serialized_start = 1390
    _STARTSYNCBLOCKASK._serialized_end = 1490
    _STOPSYNCBLOCKASK._serialized_start = 1492
    _STOPSYNCBLOCKASK._serialized_end = 1527
    _STARTSYNCEVENTASK._serialized_start = 1530
    _STARTSYNCEVENTASK._serialized_end = 1658
    _STOPSYNCEVENTASK._serialized_start = 1660
    _STOPSYNCEVENTASK._serialized_end = 1711
    _STARTSYNCORACLEASK._serialized_start = 1713
    _STARTSYNCORACLEASK._serialized_end = 1812
    _STOPSYNCORACLEASK._serialized_start = 1814
    _STOPSYNCORACLEASK._serialized_end = 1866
    _COMREPLY._serialized_start = 1868
    _COMREPLY._serialized_end = 1926
    _DATACENTER._serialized_start = 1929
    _DATACENTER._serialized_end = 2665
# @@protoc_insertion_point(module_scope)

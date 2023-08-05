#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class TExtArgumentType(object):
    Int8 = 0
    Int16 = 1
    Int32 = 2
    Int64 = 3
    Float = 4
    Double = 5
    Void = 6
    PInt8 = 7
    PInt16 = 8
    PInt32 = 9
    PInt64 = 10
    PFloat = 11
    PDouble = 12
    PBool = 13
    Bool = 14
    ArrayInt8 = 15
    ArrayInt16 = 16
    ArrayInt32 = 17
    ArrayInt64 = 18
    ArrayFloat = 19
    ArrayDouble = 20
    ArrayBool = 21
    GeoPoint = 22
    GeoLineString = 23
    Cursor = 24
    GeoPolygon = 25
    GeoMultiPolygon = 26

    _VALUES_TO_NAMES = {
        0: "Int8",
        1: "Int16",
        2: "Int32",
        3: "Int64",
        4: "Float",
        5: "Double",
        6: "Void",
        7: "PInt8",
        8: "PInt16",
        9: "PInt32",
        10: "PInt64",
        11: "PFloat",
        12: "PDouble",
        13: "PBool",
        14: "Bool",
        15: "ArrayInt8",
        16: "ArrayInt16",
        17: "ArrayInt32",
        18: "ArrayInt64",
        19: "ArrayFloat",
        20: "ArrayDouble",
        21: "ArrayBool",
        22: "GeoPoint",
        23: "GeoLineString",
        24: "Cursor",
        25: "GeoPolygon",
        26: "GeoMultiPolygon",
    }

    _NAMES_TO_VALUES = {
        "Int8": 0,
        "Int16": 1,
        "Int32": 2,
        "Int64": 3,
        "Float": 4,
        "Double": 5,
        "Void": 6,
        "PInt8": 7,
        "PInt16": 8,
        "PInt32": 9,
        "PInt64": 10,
        "PFloat": 11,
        "PDouble": 12,
        "PBool": 13,
        "Bool": 14,
        "ArrayInt8": 15,
        "ArrayInt16": 16,
        "ArrayInt32": 17,
        "ArrayInt64": 18,
        "ArrayFloat": 19,
        "ArrayDouble": 20,
        "ArrayBool": 21,
        "GeoPoint": 22,
        "GeoLineString": 23,
        "Cursor": 24,
        "GeoPolygon": 25,
        "GeoMultiPolygon": 26,
    }


class TOutputBufferSizeType(object):
    kUserSpecifiedConstantParameter = 0
    kUserSpecifiedRowMultiplier = 1
    kConstant = 2

    _VALUES_TO_NAMES = {
        0: "kUserSpecifiedConstantParameter",
        1: "kUserSpecifiedRowMultiplier",
        2: "kConstant",
    }

    _NAMES_TO_VALUES = {
        "kUserSpecifiedConstantParameter": 0,
        "kUserSpecifiedRowMultiplier": 1,
        "kConstant": 2,
    }


class TUserDefinedFunction(object):
    """
    Attributes:
     - name
     - argTypes
     - retType

    """


    def __init__(self, name=None, argTypes=None, retType=None,):
        self.name = name
        self.argTypes = argTypes
        self.retType = retType

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.argTypes = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readI32()
                        self.argTypes.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.retType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TUserDefinedFunction')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.argTypes is not None:
            oprot.writeFieldBegin('argTypes', TType.LIST, 2)
            oprot.writeListBegin(TType.I32, len(self.argTypes))
            for iter6 in self.argTypes:
                oprot.writeI32(iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.retType is not None:
            oprot.writeFieldBegin('retType', TType.I32, 3)
            oprot.writeI32(self.retType)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TUserDefinedTableFunction(object):
    """
    Attributes:
     - name
     - sizerType
     - sizerArgPos
     - inputArgTypes
     - outputArgTypes
     - sqlArgTypes

    """


    def __init__(self, name=None, sizerType=None, sizerArgPos=None, inputArgTypes=None, outputArgTypes=None, sqlArgTypes=None,):
        self.name = name
        self.sizerType = sizerType
        self.sizerArgPos = sizerArgPos
        self.inputArgTypes = inputArgTypes
        self.outputArgTypes = outputArgTypes
        self.sqlArgTypes = sqlArgTypes

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.sizerType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.sizerArgPos = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.inputArgTypes = []
                    (_etype10, _size7) = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = iprot.readI32()
                        self.inputArgTypes.append(_elem12)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.LIST:
                    self.outputArgTypes = []
                    (_etype16, _size13) = iprot.readListBegin()
                    for _i17 in range(_size13):
                        _elem18 = iprot.readI32()
                        self.outputArgTypes.append(_elem18)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.LIST:
                    self.sqlArgTypes = []
                    (_etype22, _size19) = iprot.readListBegin()
                    for _i23 in range(_size19):
                        _elem24 = iprot.readI32()
                        self.sqlArgTypes.append(_elem24)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TUserDefinedTableFunction')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.sizerType is not None:
            oprot.writeFieldBegin('sizerType', TType.I32, 2)
            oprot.writeI32(self.sizerType)
            oprot.writeFieldEnd()
        if self.sizerArgPos is not None:
            oprot.writeFieldBegin('sizerArgPos', TType.I32, 3)
            oprot.writeI32(self.sizerArgPos)
            oprot.writeFieldEnd()
        if self.inputArgTypes is not None:
            oprot.writeFieldBegin('inputArgTypes', TType.LIST, 4)
            oprot.writeListBegin(TType.I32, len(self.inputArgTypes))
            for iter25 in self.inputArgTypes:
                oprot.writeI32(iter25)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.outputArgTypes is not None:
            oprot.writeFieldBegin('outputArgTypes', TType.LIST, 5)
            oprot.writeListBegin(TType.I32, len(self.outputArgTypes))
            for iter26 in self.outputArgTypes:
                oprot.writeI32(iter26)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.sqlArgTypes is not None:
            oprot.writeFieldBegin('sqlArgTypes', TType.LIST, 6)
            oprot.writeListBegin(TType.I32, len(self.sqlArgTypes))
            for iter27 in self.sqlArgTypes:
                oprot.writeI32(iter27)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(TUserDefinedFunction)
TUserDefinedFunction.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.LIST, 'argTypes', (TType.I32, None, False), None, ),  # 2
    (3, TType.I32, 'retType', None, None, ),  # 3
)
all_structs.append(TUserDefinedTableFunction)
TUserDefinedTableFunction.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.I32, 'sizerType', None, None, ),  # 2
    (3, TType.I32, 'sizerArgPos', None, None, ),  # 3
    (4, TType.LIST, 'inputArgTypes', (TType.I32, None, False), None, ),  # 4
    (5, TType.LIST, 'outputArgTypes', (TType.I32, None, False), None, ),  # 5
    (6, TType.LIST, 'sqlArgTypes', (TType.I32, None, False), None, ),  # 6
)
fix_spec(all_structs)
del all_structs

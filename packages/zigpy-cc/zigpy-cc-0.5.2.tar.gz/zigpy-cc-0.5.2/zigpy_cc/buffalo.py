from collections.abc import Iterable

import zigpy.types
from zigpy_cc.exception import TODO
from zigpy_cc.types import AddressMode, ParameterType


class BuffaloOptions:
    def __init__(self) -> None:
        self.startIndex = None
        self.length = None


class Buffalo:
    def __init__(self, buffer, position=0) -> None:
        self.position = position
        self.buffer = buffer
        self._len = len(buffer)

    def __len__(self) -> int:
        return len(self.buffer)

    def write_parameter(self, type, value, options):
        if type == ParameterType.UINT8:
            self.write(value)
        elif type == ParameterType.UINT16:
            self.write(value, 2)
        elif type == ParameterType.UINT32:
            self.write(value, 4)
        elif type == ParameterType.IEEEADDR:
            if isinstance(value, Iterable):
                for i in value:
                    self.write(i)
            else:
                self.write(value, 8)
        elif type == ParameterType.BUFFER:
            self.buffer += value
        elif type == ParameterType.LIST_UINT8:
            for v in value:
                self.write(v)
        elif type == ParameterType.LIST_UINT16:
            for v in value:
                self.write(v, 2)
        elif type == ParameterType.LIST_NEIGHBOR_LQI:
            for v in value:
                self.write_neighbor_lqi(v)
        else:
            raise TODO(
                "write %s, value: %s, options: %s", ParameterType(type), value, options
            )

    def write(self, value, length=1, signed=False):
        self.buffer += value.to_bytes(length, "little", signed=signed)

    def write_neighbor_lqi(self, value):
        for i in value["extPanId"]:
            self.write(i)
        for i in value["extAddr"]:
            self.write(i)
        self.write(value["nwkAddr"], 2)
        self.write(
            value["deviceType"]
            | (value["rxOnWhenIdle"] * 4)
            | (value["relationship"] * 16)
        )
        self.write(value["permitJoin"])
        self.write(value["depth"])
        self.write(value["lqi"])

    def read_parameter(self, name, type, options):

        if type == ParameterType.UINT8:
            res = self.read_int()
            if name.endswith("addrmode"):
                res = AddressMode(res)
        elif type == ParameterType.UINT16:
            res = self.read_int(2)
            if (
                name.endswith("addr")
                or name.endswith("address")
                or name.endswith("addrofinterest")
            ):
                res = zigpy.types.NWK(res)
        elif type == ParameterType.UINT32:
            res = self.read_int(4)
        elif type == ParameterType.IEEEADDR:
            res = self.read_ieee_addr()
        elif ParameterType.is_buffer(type):
            type_name = ParameterType(type).name
            length = int(type_name.replace("BUFFER", "") or options.length)
            res = self.read(length)
        elif type == ParameterType.INT8:
            res = self.read_int(signed=True)
        else:
            # list types
            res = []
            if type == ParameterType.LIST_UINT8:
                for i in range(0, options.length):
                    res.append(self.read_int())
            elif type == ParameterType.LIST_UINT16:
                for i in range(0, options.length):
                    res.append(self.read_int(2))
            elif type == ParameterType.LIST_NEIGHBOR_LQI:
                for i in range(0, options.length):
                    res.append(self.read_neighbor_lqi())
            else:
                raise TODO("read type %d", type)

        return res

    def read_int(self, length=1, signed=False):
        return int.from_bytes(self.read(length), "little", signed=signed)

    def read(self, length=1):
        if self.position + length > self._len:
            raise OverflowError
        res = self.buffer[self.position : self.position + length]
        self.position += length
        return res

    def read_ieee_addr(self):
        return zigpy.types.EUI64(self.read(8))

    def read_neighbor_lqi(self):
        item = dict()
        item["extPanId"] = self.read_ieee_addr()
        item["extAddr"] = self.read_ieee_addr()
        item["nwkAddr"] = zigpy.types.NWK(self.read_int(2))

        value1 = self.read_int()
        item["deviceType"] = value1 & 0x03
        item["rxOnWhenIdle"] = (value1 & 0x0C) >> 2
        item["relationship"] = (value1 & 0x70) >> 4

        item["permitJoin"] = self.read_int() & 0x03
        item["depth"] = self.read_int()
        item["lqi"] = self.read_int()

        return item

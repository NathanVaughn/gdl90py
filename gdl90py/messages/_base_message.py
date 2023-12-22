from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Self, Type, TypeVar

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import BadIntegerSize, InvalidMessageID, UnexpectedNegative

"""
From the Specification:
> By convention, asynchronous serial communication transmits byte-wise data over the interface
> with the least-significant bit first, immediately following the Start bit. The most significant bit is
> followed by the Stop bit.

> In this document, the least significant bit of a byte is referred to as Bit 0, carries a weight of
> 1, and is depicted as the right-most bit. The most-significant bit of a byte is referred to as
> Bit 7, carries a weight of 128, and is depicted as the left-most bit.

In short, the document writes things in reverse order for each byte. To make
our lives easier, we build the data as MSB (Python-native) and flip it
at the end.
"""

T = TypeVar("T", bound=IntEnum)


class BaseMessage(ABC):
    MESSAGE_IDS = (float("nan"),)

    @abstractmethod
    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        """
        `outgoing_lsb` should be set to True if the bytes
        produced should be created with the Least Signficiant Bit first.
        """
        pass

    @classmethod
    def _clean_data(
        cls, data: bytes | bytearray | BitArray, incoming_msb: bool = False
    ) -> BitArray:
        """
        Clean incoming data to remove flag bytes, CRC, message ID(s), and unescape
        """
        if isinstance(data, (bytes, bytearray, memoryview)):
            message_ids, data = gdl90py.utils.gdl90.deconstruct(data, incoming_msb)
            if message_ids != cls.MESSAGE_IDS:
                raise InvalidMessageID(f"Invalid message ID(s) {message_ids}")

        return data

    @abstractmethod
    def deserialize(
        self, data: bytes | bytearray | BitArray, incoming_msb: bool = False
    ) -> Self:
        pass

    def _serialize_uint(
        self, value: int, bits: int, constrain: bool = True
    ) -> BitArray:
        """
        Serialize an unsigned integer.
        """
        if value < 0:
            raise UnexpectedNegative(
                "Cannot serialize negative value for unsigned integer."
            )

        if constrain:
            value = min(value, (2**bits) - 1)
        elif value > (2**bits) - 1:
            raise BadIntegerSize(
                f"{value} exceeds the maximum value for an unsigned {bits}-bit integer"
            )

        return BitArray(uint=value, length=bits)

    @classmethod
    def _deserialize_uint(cls, bitarray: BitArray) -> int:
        """
        Deserialize an unsigned integer
        """
        return bitarray.uint

    def _serialize_int(self, value: int, bits: int, constrain: bool = True) -> BitArray:
        """
        Serialize a signed integer.
        """
        if constrain:
            value = min(value, (2 ** (bits - 1)) - 1)
            value = max(value, 0 - (2 ** (bits - 1)))
        elif value > (2 ** (bits - 1)) - 1:
            raise BadIntegerSize(
                f"{value} exceeds the maximum value for a signed {bits}-bit integer"
            )
        elif value < 0 - (2 ** (bits - 1)):
            raise BadIntegerSize(
                f"{value} exceeds the minimum value for a signed {bits}-bit integer"
            )

        return BitArray(int=value, length=bits)

    @classmethod
    def _deserialize_int(cls, bitarray: BitArray) -> int:
        """
        Deserialize an signed integer
        """
        return bitarray.int

    def _serialize_resolution_uint(
        self, value: int, resolution: float, bits: int
    ) -> BitArray:
        """
        Serialize an unsigned integer with a resolution.
        """
        return self._serialize_uint(int(value / resolution), bits)

    @classmethod
    def _deserialize_resolution_uint(cls, bitarray: BitArray, resolution: float) -> int:
        """
        Deserialize an unsigned integer with a resolution.
        """
        return int(cls._deserialize_uint(bitarray) * resolution)

    def _serialize_resolution_int(
        self, value: float, resolution: float, bits: int
    ) -> BitArray:
        """
        Serialize a signed integer with a resolution.
        """
        return self._serialize_int(int(value / resolution), bits)

    @classmethod
    def _deserialize_resolution_int(cls, bitarray: BitArray, resolution: float) -> int:
        """
        Deserialize a signed integer with a resolution.
        """
        return int(cls._deserialize_resolution_float(bitarray, resolution))

    def _serialize_resolution_float(
        self, value: float, resolution: float, bits: int
    ) -> BitArray:
        """
        Serialize a signed float with a resolution.
        """
        return self._serialize_resolution_int(value, resolution, bits)

    @classmethod
    def _deserialize_resolution_float(
        cls, bitarray: BitArray, resolution: float
    ) -> float:
        """
        Deserialize a signed float with a resolution.
        """
        return cls._deserialize_int(bitarray) * resolution

    def _serialize_resolution_offset_uint(
        self, value: int, offset: int, resolution: float, bits: int
    ) -> BitArray:
        """
        Serialize an unsigned integer with an offset and resolution.
        """
        return self._serialize_resolution_uint(value + offset, resolution, bits)

    @classmethod
    def _deserialize_resolution_offset_uint(
        cls, bitarray: BitArray, offset: int, resolution: float
    ) -> int:
        """
        Deserialize an unsigned integer with an offset and resolution.
        """
        return cls._deserialize_resolution_uint(bitarray, resolution) - offset

    def _serialize_bool(self, value: bool) -> BitArray:
        """
        Serialize a boolean.
        """
        return self._serialize_uint(int(value), 1)

    @classmethod
    def _deserialize_bool(cls, bitarray: BitArray) -> bool:
        """
        Deserialize a boolean.
        """
        return bitarray.bool

    def _serialize_str(self, value: str, bits: int) -> BitArray:
        """
        Serialize a string.
        """
        # each character is 1 byte
        num_bytes = int(bits / 8)

        # pad to enough characters
        value = value.ljust(num_bytes)
        # strip extra characters
        value = value[:num_bytes]

        return BitArray(bytes=value.encode("utf-8"), length=bits)

    @classmethod
    def _deserialize_str(cls, bitarray: BitArray) -> str:
        """
        Deserialize a string.
        """
        return bitarray.bytes.decode("utf-8")

    def _serialize_enum(self, value: IntEnum, length: int) -> BitArray:
        """
        Serialize a Enum.
        """
        return self._serialize_uint(value.value, length)

    @classmethod
    def _deserialize_enum(cls, bitarray: BitArray, enum: Type[T]) -> T:
        """
        Deserialize a Enum.
        """
        return enum(cls._deserialize_uint(bitarray))

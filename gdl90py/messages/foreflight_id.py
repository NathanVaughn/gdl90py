from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.gdl90_helpers
from gdl90py.bitarray_helpers import pop_bits
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage


@dataclass(frozen=True)
class ForeFlightIDMessage(BaseMessage):
    MESSAGE_IDS = (gdl90py.gdl90_helpers.FOREFLIGHT_MESSAGE_ID, 0)

    device_serial_number: int | None
    """
    8-byte serial number.
    """
    device_name: str
    """
    8-byte device name string.
    """
    device_long_name: str | None
    """
    16-byte long device name string. If omitted, `device_name` will be used as well.
    """
    is_msl: bool
    """
    Whether or not reported altitudes are WGS84 or MSL.
    """
    version: int = 1
    """
    Version. At time of writing, should always be 1.
    """

    # constants
    VERSION_BITS = 8
    DEVICE_SERIAL_NUMBER_BITS = 64
    DEVICE_SERIAL_NUMBER_INVALID_VALUE = 0xFFFFFFFFFFFFFFFF
    DEVICE_NAME_BITS = 64
    DEVICE_LONG_NAME_BITS = 128
    RESERVED_BITS_1 = 7
    RESERVED_BITS_2 = 24

    def _serialize_version(self) -> BitArray:
        return self._serialize_uint(self.version, self.VERSION_BITS)

    @classmethod
    def _deserialize_version(cls, version_bitarray: BitArray) -> int:
        return cls._deserialize_uint(version_bitarray)

    def _serialize_device_serial_number(self) -> BitArray:
        device_serial_number = self.device_serial_number
        if device_serial_number is None:
            device_serial_number = self.DEVICE_SERIAL_NUMBER_INVALID_VALUE
        return self._serialize_uint(
            device_serial_number, self.DEVICE_SERIAL_NUMBER_BITS, constrain=False
        )

    @classmethod
    def _deserialize_device_serial_number(
        cls, device_serial_number_bitarray: BitArray
    ) -> int | None:
        if device_serial_number_bitarray.uint == cls.DEVICE_SERIAL_NUMBER_INVALID_VALUE:
            return None

        return cls._deserialize_uint(device_serial_number_bitarray)

    def _serialize_device_name(self) -> BitArray:
        return self._serialize_str(self.device_name, self.DEVICE_NAME_BITS)

    @classmethod
    def _deserialize_device_name(cls, device_name_bitarray: BitArray) -> str:
        # remove trailing whitespace
        return cls._deserialize_str(device_name_bitarray).rstrip()

    def _serialize_device_long_name(self) -> BitArray:
        device_long_name = self.device_long_name
        if device_long_name is None:
            device_long_name = self.device_name

        return self._serialize_str(device_long_name, self.DEVICE_LONG_NAME_BITS)

    @classmethod
    def _deserialize_device_long_name(cls, device_long_name_bitarray: BitArray) -> str:
        return cls._deserialize_str(device_long_name_bitarray)

    def _serialize_is_msl(self) -> BitArray:
        return self._serialize_bool(self.is_msl)

    @classmethod
    def _deserialize_is_msl(cls, is_msl_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(is_msl_bitarray)

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            self._serialize_version()
            + self._serialize_device_serial_number()
            + self._serialize_device_name()
            + self._serialize_device_long_name()
            + BitArray(uint=0, length=self.RESERVED_BITS_1)  # reserved
            + self._serialize_is_msl()
            + BitArray(uint=0, length=self.RESERVED_BITS_2)  # reserved
        )
        return gdl90py.gdl90_helpers.build(self.MESSAGE_IDS, all_data, outgoing_lsb)

    @classmethod
    def deserialize(cls, data: BitArray) -> ForeFlightIDMessage:
        version = cls._deserialize_version(pop_bits(data, cls.VERSION_BITS))
        device_serial_number = cls._deserialize_device_serial_number(
            pop_bits(data, cls.DEVICE_SERIAL_NUMBER_BITS)
        )
        device_name = cls._deserialize_device_name(pop_bits(data, cls.DEVICE_NAME_BITS))
        device_long_name = cls._deserialize_device_long_name(
            pop_bits(data, cls.DEVICE_LONG_NAME_BITS)
        )
        pop_bits(data, cls.RESERVED_BITS_1)  # reserved
        is_msl = cls._deserialize_is_msl(pop_bits(data, 1))
        pop_bits(data, cls.RESERVED_BITS_2)  # reserved

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return ForeFlightIDMessage(
            device_serial_number=device_serial_number,
            device_name=device_name,
            device_long_name=device_long_name,
            is_msl=is_msl,
            version=version,
        )

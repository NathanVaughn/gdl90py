from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import DataTooLong, UplinkDataWrongSize
from gdl90py.messages._base_message import BaseMessage
from gdl90py.utils.bitarray import pop_bits


@dataclass(frozen=True)
class BaseUATReportMessage(BaseMessage):
    time_of_reception: int | None
    """
    Time of Reception of the message in Nanoseconds, between 0 to 1 second.
    (billionths of a second)

    The complete Time of Applicability of a message is determined by combining the Time Stamp
    from the Heartbeat message (which gives the integer seconds since UTC midnight), with the
    seconds fraction found in the TOR field of the report.

    A None value represents that the TOR value is not valid
    (i.e. the ownship GDL 90 does not have sufficient timing accuracy to output a useful time value).
    """

    uplink_payload: bytes
    """
    The Uplink Data consists of the entire contents of the Uplink message received over the air.
    """

    # constants
    TIME_OF_RECEPTION_BITS = 24
    TIME_OF_RECEPTION_RESOLUTION = 80
    TIME_OF_RECEPTION_MIN = 0
    TIME_OF_RECEPTION_MAX = 100000000
    TIME_OF_RECEPTION_INVALID_VALUE = 0xFFFFFF
    UPLINK_PAYLOAD_BITS = float("nan")

    def _serialize_time_of_reception(self) -> BitArray:
        if self.time_of_reception is None or not (
            self.TIME_OF_RECEPTION_MIN
            <= self.time_of_reception
            <= self.TIME_OF_RECEPTION_MAX
        ):
            result = self._serialize_uint(
                self.TIME_OF_RECEPTION_INVALID_VALUE, self.TIME_OF_RECEPTION_BITS
            )
        else:
            result = self._serialize_resolution_uint(
                self.time_of_reception,
                self.TIME_OF_RECEPTION_RESOLUTION,
                self.TIME_OF_RECEPTION_BITS,
            )

        # time of reception has the least signficant byte first
        result.byteswap()
        return result

    @classmethod
    def _deserialize_time_of_reception(
        cls, time_of_reception_bitarray: BitArray
    ) -> int | None:
        # time of reception has the least signficant byte first
        time_of_reception_bitarray.byteswap()

        if time_of_reception_bitarray.uint == cls.TIME_OF_RECEPTION_INVALID_VALUE:
            return None

        return cls._deserialize_resolution_int(
            time_of_reception_bitarray, cls.TIME_OF_RECEPTION_RESOLUTION
        )

    def _serialize_uplink_payload(self) -> BitArray:
        bitarray = BitArray(bytes=self.uplink_payload)
        if len(bitarray) != self.UPLINK_PAYLOAD_BITS:
            raise UplinkDataWrongSize(
                f"Uplink payload is not {self.UPLINK_PAYLOAD_BITS/8} bytes"
            )
        return bitarray

    @classmethod
    def _deserialize_uplink_payload(cls, uplink_payload_bitarray: BitArray) -> bytes:
        return uplink_payload_bitarray.bytes

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            self._serialize_time_of_reception() + self._serialize_uplink_payload()
        )
        return gdl90py.utils.gdl90.build(self.MESSAGE_IDS, all_data, outgoing_lsb)  # type: ignore

    @classmethod
    def deserialize(
        cls, data: BitArray | bytes | bytearray, incoming_msb: bool = True
    ) -> Self:
        data = cls._clean_data(data, incoming_msb)

        time_of_reception = cls._deserialize_time_of_reception(
            pop_bits(data, cls.TIME_OF_RECEPTION_BITS)
        )
        uplink_payload = cls._deserialize_uplink_payload(
            pop_bits(data, cls.UPLINK_PAYLOAD_BITS)  # type: ignore
        )

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return cls(time_of_reception=time_of_reception, uplink_payload=uplink_payload)

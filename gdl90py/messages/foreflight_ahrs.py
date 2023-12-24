from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage
from gdl90py.utils.bitarray import pop_bits


@dataclass(frozen=True)
class ForeFlightAHRSMessage(BaseMessage):
    MESSAGE_IDS = (gdl90py.utils.gdl90.FOREFLIGHT_MESSAGE_ID, 1)

    roll: float | None
    """
    Degrees. Positive: right wing down. Negative: right wing up.
    """
    pitch: float | None
    """
    Degrees. Positive: nose up. Negative: nose down
    """
    is_magnetic_heading: bool | None
    """
    Whether or not the heading is true heading or magnetic heading.
    """
    heading: float | None
    """
    Heading is in degrees.
    """
    indicated_airspeed: int | None
    """
    Indicated airspeed in knots.
    """
    true_airspeed: int | None
    """
    True airspeed in knots.
    """

    # constants
    ROLL_BITS = 16
    ROLL_RESOLUTION = 1 / 10
    ROLL_MIN = -180
    ROLL_MAX = 180
    ROLL_INVALID_VALUE = 0x7FFF
    PITCH_BITS = 16
    PITCH_RESOLUTION = 1 / 10
    PITCH_MIN = -180
    PITCH_MAX = 180
    PITCH_INVALID_VALUE = 0x7FFF
    IS_MAGNETIC_HEADING_BITS = 1
    HEADING_BITS = 15
    HEADING_RESOLUTION = 1 / 10
    HEADING_MIN = -360
    HEADING_MAX = 360
    HEADING_INVALID_VALUE = 0xFFFF
    INDICATED_AIRSPEED_BITS = 16
    INDICATED_AIRSPEED_INVALID_VALUE = 0xFFFF
    TRUE_AIRSPEED_BITS = 16
    TRUE_AIRSPEED_INVALID_VALUE = 0xFFFF

    def _serialize_roll(self) -> BitArray:
        if self.roll is None or not (self.ROLL_MIN <= self.roll <= self.ROLL_MAX):
            return self._serialize_uint(self.ROLL_INVALID_VALUE, self.ROLL_BITS)

        return self._serialize_resolution_int(
            self.roll, self.ROLL_RESOLUTION, self.ROLL_BITS
        )

    @classmethod
    def _deserialize_roll(cls, roll_bitarray: BitArray) -> int | None:
        if roll_bitarray.uint == cls.ROLL_INVALID_VALUE:
            return None

        return cls._deserialize_resolution_int(roll_bitarray, cls.ROLL_RESOLUTION)

    def _serialize_pitch(self) -> BitArray:
        if self.pitch is None or not (self.PITCH_MIN <= self.pitch <= self.PITCH_MAX):
            return self._serialize_uint(self.PITCH_INVALID_VALUE, self.PITCH_BITS)

        return self._serialize_resolution_int(
            self.pitch, self.PITCH_RESOLUTION, self.PITCH_BITS
        )

    @classmethod
    def _deserialize_pitch(cls, pitch_bitarray: BitArray) -> int | None:
        if pitch_bitarray.uint == cls.PITCH_INVALID_VALUE:
            return None

        return cls._deserialize_resolution_int(pitch_bitarray, cls.PITCH_RESOLUTION)

    def _serialize_heading(self) -> BitArray:
        if (
            self.heading is None
            or not (self.HEADING_MIN <= self.heading <= self.HEADING_MAX)
            or self.is_magnetic_heading is None
        ):
            return self._serialize_uint(
                self.HEADING_INVALID_VALUE,
                self.IS_MAGNETIC_HEADING_BITS + self.HEADING_BITS,
            )

        return self._serialize_bool(
            self.is_magnetic_heading
        ) + self._serialize_resolution_int(
            self.heading, self.HEADING_RESOLUTION, self.HEADING_BITS
        )

    @classmethod
    def _deserialize_heading(
        cls, heading_bitarray: BitArray
    ) -> tuple[bool | None, int | None]:
        if heading_bitarray.uint == cls.HEADING_INVALID_VALUE:
            return None, None

        return heading_bitarray[0], cls._deserialize_resolution_int(
            heading_bitarray[cls.IS_MAGNETIC_HEADING_BITS :], cls.HEADING_RESOLUTION
        )

    def _serialize_indicated_airspeed(self) -> BitArray:
        if self.indicated_airspeed is None:
            return self._serialize_uint(
                self.INDICATED_AIRSPEED_INVALID_VALUE, self.INDICATED_AIRSPEED_BITS
            )

        return self._serialize_int(
            self.indicated_airspeed, self.INDICATED_AIRSPEED_BITS
        )

    @classmethod
    def _deserialize_indicated_airspeed(
        cls, indicated_airspeed_bitarray: BitArray
    ) -> int | None:
        if indicated_airspeed_bitarray.uint == cls.INDICATED_AIRSPEED_INVALID_VALUE:
            return None

        return cls._deserialize_int(indicated_airspeed_bitarray)

    def _serialize_true_airspeed(self) -> BitArray:
        if self.true_airspeed is None:
            return self._serialize_uint(
                self.TRUE_AIRSPEED_INVALID_VALUE, self.TRUE_AIRSPEED_BITS
            )

        return self._serialize_int(self.true_airspeed, self.TRUE_AIRSPEED_BITS)

    @classmethod
    def _deserialize_true_airspeed(cls, true_airspeed_bitarray: BitArray) -> int | None:
        if true_airspeed_bitarray.uint == cls.TRUE_AIRSPEED_INVALID_VALUE:
            return None

        return cls._deserialize_int(true_airspeed_bitarray)

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            self._serialize_roll()
            + self._serialize_pitch()
            + self._serialize_heading()
            + self._serialize_indicated_airspeed()
            + self._serialize_true_airspeed()
        )
        return gdl90py.utils.gdl90.build(self.MESSAGE_IDS, all_data, outgoing_lsb)

    @classmethod
    def deserialize(
        cls, data: BitArray | bytes | bytearray, incoming_msb: bool = True
    ) -> ForeFlightAHRSMessage:
        data = cls._clean_data(data, incoming_msb)

        roll = cls._deserialize_roll(pop_bits(data, cls.ROLL_BITS))
        pitch = cls._deserialize_pitch(pop_bits(data, cls.PITCH_BITS))
        is_magnetic_heading, heading = cls._deserialize_heading(
            pop_bits(data, cls.IS_MAGNETIC_HEADING_BITS + cls.HEADING_BITS)
        )
        indicated_airspeed = cls._deserialize_indicated_airspeed(
            pop_bits(data, cls.INDICATED_AIRSPEED_BITS)
        )
        true_airspeed = cls._deserialize_true_airspeed(
            pop_bits(data, cls.TRUE_AIRSPEED_BITS)
        )

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return ForeFlightAHRSMessage(
            roll=roll,
            pitch=pitch,
            is_magnetic_heading=is_magnetic_heading,
            heading=heading,
            indicated_airspeed=indicated_airspeed,
            true_airspeed=true_airspeed,
        )

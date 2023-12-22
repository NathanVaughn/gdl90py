from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage
from gdl90py.utils.bitarray import pop_bits


@dataclass(frozen=True)
class OwnshipGeometricAltitudeMessage(BaseMessage):
    MESSAGE_IDS = (11,)

    geo_altitude: int
    """
    Feet, above WGS84 or as MSL.
    """
    vertical_warning_indicator: bool
    """
    True if a position alarm is present, or if fault detection is not available
    """
    vertical_figure_of_merit: int | None = None
    """
    Vertical position accuracy in meters.
    """

    # constants
    GEO_ALTITUDE_RESOLUTION = 5
    GEO_ALTITUDE_BITS = 16
    VERTICAL_FIGURE_OF_MERIT_UNAVAILABLE = 0x7FFF
    VERTICAL_FIGURE_OF_MERIT_MAX = 32766
    VERTICAL_FIGURE_OF_MERIT_MAX_VALUE = 0x7FFE
    VERTICAL_FIGURE_OF_MERIT_BITS = 15

    def _serialize_geo_altitude(self) -> BitArray:
        return self._serialize_resolution_int(
            self.geo_altitude, self.GEO_ALTITUDE_RESOLUTION, self.GEO_ALTITUDE_BITS
        )

    @classmethod
    def _deserialize_geo_altitude(cls, geo_altitude_bitarray: BitArray) -> int:
        return cls._deserialize_resolution_int(
            geo_altitude_bitarray, cls.GEO_ALTITUDE_RESOLUTION
        )

    def _serialize_vertical_warning_indicator(self) -> BitArray:
        return self._serialize_bool(self.vertical_warning_indicator)

    @classmethod
    def _deserialize_vertical_warning_indicator(
        cls, vertical_warning_indicator_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(vertical_warning_indicator_bitarray)

    def _serialize_vertical_figure_of_merit(self) -> BitArray:
        if self.vertical_figure_of_merit is None:
            vertical_figure_of_merit_normalized = (
                self.VERTICAL_FIGURE_OF_MERIT_UNAVAILABLE
            )
        elif self.vertical_figure_of_merit > self.VERTICAL_FIGURE_OF_MERIT_MAX:
            vertical_figure_of_merit_normalized = (
                self.VERTICAL_FIGURE_OF_MERIT_MAX_VALUE
            )
        else:
            vertical_figure_of_merit_normalized = self.vertical_figure_of_merit

        return BitArray(
            uint=vertical_figure_of_merit_normalized,
            length=self.VERTICAL_FIGURE_OF_MERIT_BITS,
        )

    @classmethod
    def _deserialize_vertical_figure_of_merit(
        cls, vertical_figure_of_merit_bitarray: BitArray
    ) -> int | None:
        vertical_figure_of_merit = vertical_figure_of_merit_bitarray.uint
        if vertical_figure_of_merit == cls.VERTICAL_FIGURE_OF_MERIT_UNAVAILABLE:
            vertical_figure_of_merit = None
        elif vertical_figure_of_merit == cls.VERTICAL_FIGURE_OF_MERIT_MAX_VALUE:
            vertical_figure_of_merit = cls.VERTICAL_FIGURE_OF_MERIT_MAX

        return vertical_figure_of_merit

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            self._serialize_geo_altitude()
            + self._serialize_vertical_warning_indicator()
            + self._serialize_vertical_figure_of_merit()
        )
        return gdl90py.utils.gdl90.build(self.MESSAGE_IDS, all_data, outgoing_lsb)

    @classmethod
    def deserialize(
        cls, data: BitArray | bytes | bytearray, incoming_msb: bool = True
    ) -> OwnshipGeometricAltitudeMessage:
        data = cls._clean_data(data, incoming_msb)

        geo_altitude = cls._deserialize_geo_altitude(
            pop_bits(data, cls.GEO_ALTITUDE_BITS)
        )
        vertical_warning_indicator = cls._deserialize_vertical_warning_indicator(
            pop_bits(data, 1)
        )

        vertical_figure_of_merit = cls._deserialize_vertical_figure_of_merit(
            pop_bits(data, cls.VERTICAL_FIGURE_OF_MERIT_BITS)
        )

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return OwnshipGeometricAltitudeMessage(
            geo_altitude=geo_altitude,
            vertical_warning_indicator=vertical_warning_indicator,
            vertical_figure_of_merit=vertical_figure_of_merit,
        )

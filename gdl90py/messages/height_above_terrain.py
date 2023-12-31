from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage
from gdl90py.utils.bitarray import pop_bits


@dataclass(frozen=True)
class HeightAboveTerrainMessage(BaseMessage):
    MESSAGE_IDS = (9,)

    height_above_terrain: int | None
    """
    Height above terrain in feet.
    """

    # constants
    HEIGHT_ABOVE_TERRAIN_BITS = 16
    HEIGHT_ABOVE_TERRAIN_INVALID_VALUE = 0x8000

    def _serialize_height_above_terrain(self) -> BitArray:
        if self.height_above_terrain is None:
            return self._serialize_uint(
                self.HEIGHT_ABOVE_TERRAIN_INVALID_VALUE, self.HEIGHT_ABOVE_TERRAIN_BITS
            )
        return self._serialize_int(
            self.height_above_terrain, self.HEIGHT_ABOVE_TERRAIN_BITS
        )

    @classmethod
    def _deserialize_height_above_terrain(
        cls, height_above_terrain_bitarray: BitArray
    ) -> int | None:
        if height_above_terrain_bitarray.uint == cls.HEIGHT_ABOVE_TERRAIN_INVALID_VALUE:
            return None

        return cls._deserialize_int(height_above_terrain_bitarray)

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        return gdl90py.utils.gdl90.build(
            self.MESSAGE_IDS, self._serialize_height_above_terrain(), outgoing_lsb
        )

    @classmethod
    def deserialize(
        cls, data: BitArray | bytes | bytearray, incoming_msb: bool = True
    ) -> HeightAboveTerrainMessage:
        data = cls._clean_data(data, incoming_msb)

        height_above_terrain = cls._deserialize_height_above_terrain(
            pop_bits(data, cls.HEIGHT_ABOVE_TERRAIN_BITS)
        )

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return HeightAboveTerrainMessage(height_above_terrain=height_above_terrain)

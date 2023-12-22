from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage
from gdl90py.utils.bitarray import pop_bits


@dataclass(frozen=True)
class InitializationMessage(BaseMessage):
    MESSAGE_IDS = (2,)

    audio_test: bool
    """
    Audio test requested.
    """
    audio_inhibit: bool
    """
    Audio inhibited.
    """
    CDTI_ok: bool
    """
    Cockpit traffic display is available.
    """
    CSA_audio_disable: bool
    """
    CSA audio has been disabled by the flight crew.
    """
    CSA_disable: bool
    """
    CSA traffic alerts have been disabled by the flight crew.
    """

    # constants
    RESERVED_1_BITS = 1
    RESERVED_2_BITS = 4
    RESERVED_3_BITS = 6

    @classmethod
    def _deserialize_audio_test(cls, audio_test_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(audio_test_bitarray)

    def _serialize_audio_test(self) -> BitArray:
        return self._serialize_bool(self.audio_test)

    @classmethod
    def _deserialize_audio_inhibit(cls, audio_inhibit_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(audio_inhibit_bitarray)

    def _serialize_audio_inhibit(self) -> BitArray:
        return self._serialize_bool(self.audio_inhibit)

    @classmethod
    def _deserialize_CDTI_ok(cls, CDTI_ok_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(CDTI_ok_bitarray)

    def _serialize_CDTI_ok(self) -> BitArray:
        return self._serialize_bool(self.CDTI_ok)

    @classmethod
    def _deserialize_CSA_audio_disable(
        cls, CSA_audio_disable_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(CSA_audio_disable_bitarray)

    def _serialize_CSA_audio_disable(self) -> BitArray:
        return self._serialize_bool(self.CSA_audio_disable)

    @classmethod
    def _deserialize_CSA_disable(cls, CSA_disable_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(CSA_disable_bitarray)

    def _serialize_CSA_disable(self) -> BitArray:
        return self._serialize_bool(self.CSA_disable)

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            BitArray(uint=0, length=self.RESERVED_1_BITS)  # reserved
            + self._serialize_audio_test()
            + BitArray(uint=0, length=self.RESERVED_2_BITS)  # reserved
            + self._serialize_audio_inhibit()
            + self._serialize_CDTI_ok()
            + BitArray(uint=0, length=self.RESERVED_3_BITS)  # reserved
            + self._serialize_CSA_audio_disable()
            + self._serialize_CSA_disable()
        )
        return gdl90py.utils.gdl90.build(self.MESSAGE_IDS, all_data, outgoing_lsb)

    @classmethod
    def deserialize(cls, data: BitArray) -> InitializationMessage:
        pop_bits(data, cls.RESERVED_1_BITS)  # reserved
        audio_test = cls._deserialize_audio_test(pop_bits(data, 1))
        pop_bits(data, cls.RESERVED_2_BITS)  # reserved
        audio_inhibit = cls._deserialize_audio_inhibit(pop_bits(data, 1))
        CDTI_ok = cls._deserialize_CDTI_ok(pop_bits(data, 1))
        pop_bits(data, cls.RESERVED_3_BITS)  # reserved
        CSA_audio_disable = cls._deserialize_CSA_audio_disable(pop_bits(data, 1))
        CSA_disable = cls._deserialize_CSA_disable(pop_bits(data, 1))

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return InitializationMessage(
            audio_test=audio_test,
            audio_inhibit=audio_inhibit,
            CDTI_ok=CDTI_ok,
            CSA_audio_disable=CSA_audio_disable,
            CSA_disable=CSA_disable,
        )

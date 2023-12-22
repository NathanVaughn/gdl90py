from enum import IntEnum
from typing import Type

import pytest
from bitstring import BitArray

from gdl90py.enums import EmergencyPriorityCode, EmitterCategory
from gdl90py.exceptions import BadIntegerSize, UnexpectedNegative
from gdl90py.messages._base_message import BaseMessage


class TestMessage(BaseMessage):
    def serialize(self, outgoing_lsb: bool = True) -> None:
        pass

    def deserialize(self, data: BitArray) -> None:
        pass


@pytest.mark.parametrize(
    "value, bits, constrain, expected",
    [
        (10, 8, True, BitArray("0b00001010")),
        (255, 8, False, BitArray("0b11111111")),
        (256, 8, True, BitArray("0b11111111")),
        (1000, 16, True, BitArray("0b0000001111101000")),
    ],
)
def test__serialize_uint(value: int, bits: int, constrain: bool, expected: BitArray):
    assert TestMessage()._serialize_uint(value, bits, constrain) == expected


@pytest.mark.parametrize(
    "value, bits, constrain, expected",
    [
        (-1, 8, True, UnexpectedNegative),
        (256, 8, False, BadIntegerSize),
    ],
)
def test__serialize_uint_fail(
    value: int, bits: int, constrain: bool, expected: Type[Exception]
):
    with pytest.raises(expected):
        TestMessage()._serialize_uint(value, bits, constrain)


@pytest.mark.parametrize(
    "bitarray, expected",
    [
        (BitArray("0b00001010"), 10),
        (BitArray("0b11111111"), 255),
        (BitArray("0b0000001111101000"), 1000),
    ],
)
def test__deserialize_uint(bitarray: BitArray, expected: int):
    assert TestMessage._deserialize_uint(bitarray) == expected


@pytest.mark.parametrize(
    "value, bits, constrain, expected",
    [
        (10, 8, True, BitArray("0b00001010")),
        (-10, 8, False, BitArray("0b11110110")),
        (256, 8, True, BitArray("0b01111111")),
        (-256, 8, True, BitArray("0b10000000")),
        (127, 8, False, BitArray("0b01111111")),
        (-128, 8, False, BitArray("0b10000000")),
        (1000, 16, True, BitArray("0b0000001111101000")),
    ],
)
def test__serialize_int(value: int, bits: int, constrain: bool, expected: BitArray):
    assert TestMessage()._serialize_int(value, bits, constrain) == expected


@pytest.mark.parametrize(
    "value, bits",
    [
        (-129, 8),
        (128, 8),
    ],
)
def test__serialize_int_fail(value: int, bits: int):
    with pytest.raises(BadIntegerSize):
        TestMessage()._serialize_int(value, bits, False)


@pytest.mark.parametrize(
    "bitarray, expected",
    [
        (BitArray("0b00001010"), 10),
        (BitArray("0b11110110"), -10),
        (BitArray("0b01111111"), 127),
        (BitArray("0b10000000"), -128),
        (BitArray("0b0000001111101000"), 1000),
    ],
)
def test__deserialize_int(bitarray: BitArray, expected: int):
    assert TestMessage._deserialize_int(bitarray) == expected


@pytest.mark.parametrize(
    "value, resolution, bits, expected",
    [
        (200, 10, 8, BitArray("0b00010100")),
        (450, 50, 8, BitArray("0b00001001")),
        (3, 1.5, 8, BitArray("0b00000010")),
    ],
)
def test__serialize_resolution_uint(
    value: int, resolution: float, bits: int, expected: BitArray
):
    assert TestMessage()._serialize_resolution_uint(value, resolution, bits) == expected


@pytest.mark.parametrize(
    "bitarray, resolution, expected",
    [
        (BitArray("0b00010100"), 10, 200),
        (BitArray("0b00001001"), 50, 450),
        (BitArray("0b00000010"), 1.5, 3),
    ],
)
def test__deserialize_resolution_uint(
    bitarray: BitArray,
    resolution: float,
    expected: int,
):
    assert TestMessage._deserialize_resolution_uint(bitarray, resolution) == expected


@pytest.mark.parametrize(
    "value, resolution, bits, expected",
    [
        (200, 10, 8, BitArray("0b00010100")),
        (450, 50, 8, BitArray("0b00001001")),
        (3, 1.5, 8, BitArray("0b00000010")),
        (-200, 10, 8, BitArray("0b11101100")),
        (-450, 50, 8, BitArray("0b11110111")),
        (-3, 1.5, 8, BitArray("0b11111110")),
    ],
)
def test__serialize_resolution_int(
    value: int, resolution: float, bits: int, expected: BitArray
):
    assert TestMessage()._serialize_resolution_int(value, resolution, bits) == expected


@pytest.mark.parametrize(
    "bitarray, resolution, expected",
    [
        (BitArray("0b00010100"), 10, 200),
        (BitArray("0b00001001"), 50, 450),
        (BitArray("0b00000010"), 1.5, 3),
        (BitArray("0b11101100"), 10, -200),
        (BitArray("0b11110111"), 50, -450),
        (BitArray("0b11111110"), 1.5, -3),
    ],
)
def test__deserialize_resolution_int(
    bitarray: BitArray,
    resolution: float,
    expected: int,
):
    assert TestMessage._deserialize_resolution_int(bitarray, resolution) == expected


@pytest.mark.parametrize(
    "value, offset, resolution, bits, expected",
    [
        (200, 20, 10, 8, BitArray("0b00010110")),
        (450, 100, 50, 8, BitArray("0b00001011")),
        (3, 2, 1, 8, BitArray("0b00000101")),
    ],
)
def test__serialize_resolution_offset_uint(
    value: int, offset: int, resolution: float, bits: int, expected: BitArray
):
    assert (
        TestMessage()._serialize_resolution_offset_uint(value, offset, resolution, bits)
        == expected
    )


@pytest.mark.parametrize(
    "bitarray, offset, resolution, expected",
    [
        (BitArray("0b00010110"), 20, 10, 200),
        (BitArray("0b00001011"), 100, 50, 450),
        (BitArray("0b00000101"), 2, 1, 3),
    ],
)
def test__deserialize_resolution_offset_uint(
    bitarray: BitArray,
    offset: int,
    resolution: float,
    expected: int,
):
    assert (
        TestMessage._deserialize_resolution_offset_uint(bitarray, offset, resolution)
        == expected
    )


def test__serialize_bool():
    assert TestMessage()._serialize_bool(True) == BitArray("0b1")
    assert TestMessage()._serialize_bool(False) == BitArray("0b0")


def test__deserialize_bool():
    assert TestMessage._deserialize_bool(BitArray("0b1")) is True
    assert TestMessage._deserialize_bool(BitArray("0b0")) is False


@pytest.mark.parametrize(
    "value, bits, expected",
    [
        ("N12345", 48, BitArray("0x4e3132333435")),
        ("too long", 16, BitArray("0x746f")),
        ("too short", 128, BitArray("0x746f6f2073686f727420202020202020")),
        ("", 8, BitArray("0x20")),
    ],
)
def test__serialize_str(value: str, bits: int, expected: BitArray):
    assert TestMessage()._serialize_str(value, bits) == expected


@pytest.mark.parametrize(
    "bitarray, expected",
    [
        (BitArray("0x4e3132333435"), "N12345"),
        (BitArray("0x746f"), "to"),
        (BitArray("0x746f6f2073686f727420202020202020"), "too short       "),
        (BitArray("0x20"), " "),
    ],
)
def test__deserialize_str(
    bitarray: BitArray,
    expected: int,
):
    assert TestMessage._deserialize_str(bitarray) == expected


@pytest.mark.parametrize(
    "value, length, expected",
    [
        (EmitterCategory.heavy, 8, BitArray("0x05")),
        (EmitterCategory.line_obstacle, 8, BitArray("0x15")),
        (EmergencyPriorityCode.no_communication, 8, BitArray("0x04")),
        (EmergencyPriorityCode.no_emergency, 8, BitArray("0x00")),
    ],
)
def test__serialize_enum(value: IntEnum, length: int, expected: BitArray):
    assert TestMessage()._serialize_enum(value, length) == expected


@pytest.mark.parametrize(
    "bitarray, enum, expected",
    [
        (BitArray("0x05"), EmitterCategory, EmitterCategory.heavy),
        (BitArray("0x15"), EmitterCategory, EmitterCategory.line_obstacle),
        (
            BitArray("0x04"),
            EmergencyPriorityCode,
            EmergencyPriorityCode.no_communication,
        ),
        (BitArray("0x00"), EmergencyPriorityCode, EmergencyPriorityCode.no_emergency),
    ],
)
def test__deserialize_enum(
    bitarray: BitArray,
    enum: Type[IntEnum],
    expected: IntEnum,
):
    assert TestMessage._deserialize_enum(bitarray, enum) == expected

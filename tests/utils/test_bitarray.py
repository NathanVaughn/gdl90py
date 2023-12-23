import pytest
from bitstring import BitArray

from gdl90py.utils.bitarray import (
    lsb,
    lsb_bytearray,
    lsb_bytes,
    lsb_int,
    pop_bits,
    print_hex,
)


def test_pop_bits():
    bitarray = BitArray(bin="11110000")
    result = pop_bits(bitarray, 4)
    assert result.bin == "1111"
    assert bitarray.bin == "0000"


def test_lsb():
    bitarray = BitArray(hex="0x1234")
    result = lsb(bitarray)
    assert result.hex == "482c"


def test_lsb_bytes():
    input_bytes = b"\x12\x34"
    result = lsb_bytes(input_bytes)
    assert result == b"\x48\x2c"


def test_lsb_bytearray():
    input_bytearray = bytearray(b"\x12\x34")
    result = lsb_bytearray(input_bytearray)
    assert result == bytearray(b"\x48\x2c")


def test_lsb_int():
    input_int = 123
    result = lsb_int(input_int)
    assert result == 222


@pytest.mark.parametrize(
    "input_, expected",
    ((b"\x12\x34", "0x12 0x34"), (BitArray(bytes=b"\x12\x34"), "0x12 0x34")),
)
def test_print_hex(capsys, input_: bytes | BitArray, expected: str):
    print_hex(input_)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

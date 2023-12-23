import pytest
from bitstring import BitArray

import gdl90py.utils.gdl90
from gdl90py.exceptions import InvalidCRC, MissingFlagBytes


def test_crc_table():
    table = gdl90py.utils.gdl90.crc_table()
    assert isinstance(table, list)
    assert len(table) == 256
    assert isinstance(table[0], int)


def test_compute_crc():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = gdl90py.utils.gdl90.compute_crc(data)
    assert isinstance(crc, bytes)
    assert len(crc) == 2
    assert crc == b"\xB3\x8B"


def test_check_crc_valid():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = b"\xB3\x8B"
    gdl90py.utils.gdl90.check_crc(data, crc)


def test_check_crc_invalid():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = b"\xB3\x8C"
    with pytest.raises(InvalidCRC):
        gdl90py.utils.gdl90.check_crc(data, crc)


def test_escape_no_escape_chars():
    data = b"\x01\x02\x03\x04\x05"
    expected = bytearray(data)
    assert gdl90py.utils.gdl90.escape(data) == expected


def test_escape_single_escape_char():
    data = b"\x01\x02\x7D\x04\x05"
    expected = bytearray(b"\x01\x02\x7D\x5d\x04\x05")
    assert gdl90py.utils.gdl90.escape(data) == expected


def test_escape_multiple_escape_chars():
    data = b"\x01\x7D\x02\x7E\x03\x7D\x04\x7E"
    expected = bytearray(b"\x01\x7D\x5D\x02\x7D\x5E\x03\x7D\x5D\x04\x7D\x5E")
    assert gdl90py.utils.gdl90.escape(data) == expected


def test_escape_empty_data():
    data = b""
    expected = bytearray()
    assert gdl90py.utils.gdl90.escape(data) == expected


def test_unescape_no_escape_chars():
    data = b"\x01\x02\x03\x04\x05"
    expected = bytearray(data)
    assert gdl90py.utils.gdl90.unescape(data) == expected


def test_unescape_single_escape_char():
    data = b"\x01\x02\x7D\x5d\x04\x05"
    expected = bytearray(b"\x01\x02\x7D\x04\x05")
    assert gdl90py.utils.gdl90.unescape(data) == expected


def test_unescape_multiple_escape_chars():
    data = b"\x01\x7D\x5D\x02\x7D\x5E\x03\x7D\x5D\x04\x7D\x5E"
    expected = bytearray(b"\x01\x7D\x02\x7E\x03\x7D\x04\x7E")
    assert gdl90py.utils.gdl90.unescape(data) == expected


def test_unescape_empty_data():
    data = b""
    expected = bytearray()
    assert gdl90py.utils.gdl90.unescape(data) == expected


def test_build_outgoing_lsb():
    message_ids = (0x00,)
    data = b"\x01\x02\x03\x04\x05"
    expected_forwards = b"\x7E\x00\x01\x02\x03\x04\x05\x34\x65\x7E"
    expected_backwards = b"\x7E\x00\x80\x40\xc0\x20\xa0\x2c\xa6\x7E"
    assert (
        gdl90py.utils.gdl90.build(message_ids, BitArray(bytes=data), outgoing_lsb=False)
        == expected_forwards
    )
    assert (
        gdl90py.utils.gdl90.build(message_ids, BitArray(bytes=data), outgoing_lsb=True)
        == expected_backwards
    )


def test_deconstruct_missing_flag_bytes():
    data = b"\x01\x02\x03\x04\x05"
    with pytest.raises(MissingFlagBytes):
        gdl90py.utils.gdl90.deconstruct(data, incoming_msb=False)


def test_deconstruct_incoming_msb_false():
    data = b"\x7E\x40\x82\x80\xC2\x86\x7E"
    expected = ((0x02,), BitArray(bytes=b"\x41\x01"))
    assert gdl90py.utils.gdl90.deconstruct(data, incoming_msb=False) == expected


def test_deconstruct_invalid_crc():
    data = b"\x7E\x40\x82\x80\xC2\x87\x7E"
    with pytest.raises(InvalidCRC):
        gdl90py.utils.gdl90.deconstruct(data, incoming_msb=False)

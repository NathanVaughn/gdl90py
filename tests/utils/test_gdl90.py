from gdl90py.utils.gdl90 import check_crc, compute_crc, crc_table, escape, unescape


def test_crc_table():
    table = crc_table()
    assert isinstance(table, list)
    assert len(table) == 256
    assert isinstance(table[0], int)


def test_compute_crc():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = compute_crc(data)
    assert isinstance(crc, bytes)
    assert len(crc) == 2
    assert crc == b"\xB3\x8B"


def test_check_crc_valid():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = b"\xB3\x8B"
    assert check_crc(data, crc) is True


def test_check_crc_invalid():
    data = b"\x00\x81\x41\xDB\xD0\x08\x02"
    crc = b"\xB3\x8C"
    assert check_crc(data, crc) is False


def test_escape_no_escape_chars():
    data = b"\x01\x02\x03\x04\x05"
    expected = bytearray(data)
    assert escape(data) == expected


def test_escape_single_escape_char():
    data = b"\x01\x02\x7D\x04\x05"
    expected = bytearray(b"\x01\x02\x7D\x5d\x04\x05")
    assert escape(data) == expected


def test_escape_multiple_escape_chars():
    data = b"\x01\x7D\x02\x7E\x03\x7D\x04\x7E"
    expected = bytearray(b"\x01\x7D\x5D\x02\x7D\x5E\x03\x7D\x5D\x04\x7D\x5E")
    assert escape(data) == expected


def test_escape_empty_data():
    data = b""
    expected = bytearray()
    assert escape(data) == expected


def test_unescape_no_escape_chars():
    data = b"\x01\x02\x03\x04\x05"
    expected = bytearray(data)
    assert unescape(data) == expected


def test_unescape_single_escape_char():
    data = b"\x01\x02\x7D\x5d\x04\x05"
    expected = bytearray(b"\x01\x02\x7D\x04\x05")
    assert unescape(data) == expected


def test_unescape_multiple_escape_chars():
    data = b"\x01\x7D\x5D\x02\x7D\x5E\x03\x7D\x5D\x04\x7D\x5E"
    expected = bytearray(b"\x01\x7D\x02\x7E\x03\x7D\x04\x7E")
    assert unescape(data) == expected


def test_unescape_empty_data():
    data = b""
    expected = bytearray()
    assert unescape(data) == expected

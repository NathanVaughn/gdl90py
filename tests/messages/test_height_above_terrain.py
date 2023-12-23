import pytest

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.height_above_terrain import HeightAboveTerrainMessage


def test_height_above_terrain_testcase():
    hat = HeightAboveTerrainMessage(256)
    data = hat.serialize(outgoing_lsb=False)
    assert data[2] == 0x01
    assert data[3] == 0x00


def test_height_above_terrain_serialize():
    hat = HeightAboveTerrainMessage(256)
    assert hat.serialize(outgoing_lsb=False) == b"\x7e\x09\x01\x00\x29\x90\x7e"


def test_height_above_terrain_deserialize():
    hat = HeightAboveTerrainMessage(256)
    assert hat == HeightAboveTerrainMessage.deserialize(b"\x7e\x09\x01\x00\x29\x90\x7e")


def test_height_above_terrain_invalid_serialize():
    hat = HeightAboveTerrainMessage(None)
    assert hat.serialize(outgoing_lsb=False) == b"\x7e\x09\x80\x00\x29\x11\x7e"


def test_height_above_terrain_invalid_deserialize():
    hat = HeightAboveTerrainMessage(None)
    assert hat == HeightAboveTerrainMessage.deserialize(b"\x7e\x09\x80\x00\x29\x11\x7e")


def test_height_above_terrain_deserialize_too_long():
    with pytest.raises(DataTooLong):
        HeightAboveTerrainMessage.deserialize(b"\x7e\x09\x80\x00\x00\x10\x2b\x7e")

from gdl90py.messages.height_above_terrain import HeightAboveTerrainMessage


def test_height_above_terrain_serialize():
    hat = HeightAboveTerrainMessage(256)
    data = hat.serialize(outgoing_lsb=False)
    assert data[2] == 0x01
    assert data[3] == 0x00

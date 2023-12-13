import pytest
from bitstring import BitArray

from gdl90py.messages.ownship_geometric_altitude import OwnshipGeometricAltitudeMessage


@pytest.mark.parametrize("ga, expected", ((-1000, 0xFF38), (0, 0x0000), (1000, 0x00C8)))
def test_geo_altitude_serialize(ga: int, expected: int):
    o = OwnshipGeometricAltitudeMessage(ga, False, None)
    assert o._serialize_geo_altitude().uint == expected


@pytest.mark.parametrize(
    "gahex, expected", (("0xFF38", -1000), ("0x0000", 0), ("0x00C8", 1000))
)
def test_geo_altitude_deserialize(gahex: str, expected: int):
    assert (
        OwnshipGeometricAltitudeMessage._deserialize_geo_altitude(BitArray(hex=gahex))
        == expected
    )


@pytest.mark.parametrize(
    "wi, vfom, expected",
    (
        (True, None, 0xFFFF),
        (False, 40000, 0x7FFE),
        (False, 10, 0x000A),
        (True, 50, 0x8032),
    ),
)
def test_vertical_metrics_serialize(wi: bool, vfom: int, expected: int):
    o = OwnshipGeometricAltitudeMessage(500, wi, vfom)
    assert (
        o._serialize_vertical_warning_indicator()
        + o._serialize_vertical_figure_of_merit()
    ).uint == expected


@pytest.mark.parametrize(
    "vmhex, expected_wi, expected_vfom",
    (
        ("0xFFFF", True, None),
        ("0x7FFE", False, 32766),
        ("0x000A", False, 10),
        ("0x8032", True, 50),
    ),
)
def test_vertical_metrics_deserialize(
    vmhex: str, expected_wi: bool, expected_vfom: int
):
    bitarray = BitArray(hex=vmhex)
    assert (
        OwnshipGeometricAltitudeMessage._deserialize_vertical_warning_indicator(
            bitarray[0:1]
        )
        == expected_wi
    )
    assert (
        OwnshipGeometricAltitudeMessage._deserialize_vertical_figure_of_merit(
            bitarray[1:]
        )
        == expected_vfom
    )

import pytest
from bitstring import BitArray

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.ownship_geometric_altitude import OwnshipGeometricAltitudeMessage


def test_ownship_geometric_altitude_serialize():
    oga = OwnshipGeometricAltitudeMessage(500, False, None)
    assert oga.serialize(outgoing_lsb=False) == b"\x7e\x0b\x00\x64\x7f\xff\x2c\xa3\x7e"


def test_ownship_geometric_altitude_deserialize():
    oga = OwnshipGeometricAltitudeMessage(500, False, None)
    assert oga == OwnshipGeometricAltitudeMessage.deserialize(
        b"\x7e\x0b\x00\x64\x7f\xff\x2c\xa3\x7e"
    )


def test_ownship_geometric_altitude_deserialize_too_long():
    with pytest.raises(DataTooLong):
        OwnshipGeometricAltitudeMessage.deserialize(
            b"\x7e\x0b\x00\x64\x7f\xff\x00\x89\xa9\x7e"
        )


@pytest.mark.parametrize(
    "ga, expected", ((-1000, b"\xff\x38"), (0, b"\x00\x00"), (1000, b"\x00\xc8"))
)
def test_geo_altitude_serialize(ga: int, expected: bytes):
    oga = OwnshipGeometricAltitudeMessage(ga, False, None)
    assert oga.serialize(outgoing_lsb=False)[2:4] == expected


@pytest.mark.parametrize(
    "gabytes, expected", ((b"\xff\x38", -1000), (b"\x00\x00", 0), (b"\x00\xc8", 1000))
)
def test_geo_altitude_deserialize(gabytes: bytes, expected: int):
    oga = OwnshipGeometricAltitudeMessage(expected, False, None)
    assert oga == OwnshipGeometricAltitudeMessage.deserialize(
        BitArray(bytes=gabytes + b"\x7f\xff")
    )


@pytest.mark.parametrize(
    "wi, vfom, expected",
    (
        (True, None, b"\xff\xff"),
        (False, 40000, b"\x7f\xfe"),
        (False, 10, b"\x00\x0a"),
        (True, 50, b"\x80\x32"),
    ),
)
def test_vertical_metrics_serialize(wi: bool, vfom: int, expected: bytes):
    oga = OwnshipGeometricAltitudeMessage(500, wi, vfom)
    assert oga.serialize(outgoing_lsb=False)[4:6] == expected


@pytest.mark.parametrize(
    "vmbytes, expected_wi, expected_vfom",
    (
        (b"\xff\xff", True, None),
        (b"\x7f\xfe", False, 32766),
        (b"\x00\x0a", False, 10),
        (b"\x80\x32", True, 50),
    ),
)
def test_vertical_metrics_deserialize(
    vmbytes: bytes, expected_wi: bool, expected_vfom: int
):
    oga = OwnshipGeometricAltitudeMessage(500, expected_wi, expected_vfom)
    assert oga == OwnshipGeometricAltitudeMessage.deserialize(
        BitArray(bytes=b"\x00\x64" + vmbytes)
    )

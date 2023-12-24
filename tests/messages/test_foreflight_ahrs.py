import pytest

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.foreflight_ahrs import ForeFlightAHRSMessage


def test_foreflight_ahrs_serialize():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert (
        ffa.serialize(outgoing_lsb=False)
        == b"\x7e\x65\x01\x01\xc2\x01\x2c\x83\x20\x00\x64\x00\x78\x26\x19\x7e"
    )


def test_foreflight_ahrs_deserialize():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x01\xc2\x01\x2c\x83\x20\x00\x64\x00\x78\x26\x19\x7e"
    )


@pytest.mark.parametrize("roll", [None, -181, 181, -360, 360])
def test_foreflight_ahrs_serialize_invalid_roll(roll: float | None):
    ffa = ForeFlightAHRSMessage(
        roll=roll,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa.serialize(outgoing_lsb=False)[3:5] == b"\x7f\xff"


def test_foreflight_ahrs_deserialize_invalid_roll():
    ffa = ForeFlightAHRSMessage(
        roll=None,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x7f\xff\x01\x2c\x83\x20\x00\x64\x00\x78\xbc\x84\x7e"
    )


@pytest.mark.parametrize("pitch", [None, -181, 181, -360, 360])
def test_foreflight_ahrs_serialize_invalid_pitch(pitch: float | None):
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=pitch,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa.serialize(outgoing_lsb=False)[5:7] == b"\x7f\xff"


def test_foreflight_ahrs_deserialize_invalid_pitch():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=None,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x01\xc2\x7f\xff\x83\x20\x00\x64\x00\x78\x29\x05\x7e"
    )


@pytest.mark.parametrize("heading", [None, -361, 361, -450, 450])
def test_foreflight_ahrs_serialize_invalid_heading(heading: float | None):
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=heading,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa.serialize(outgoing_lsb=False)[7:9] == b"\xff\xff"


def test_foreflight_ahrs_serialize_invalid_is_magnetic_heading():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=None,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa.serialize(outgoing_lsb=False)[7:9] == b"\xff\xff"


def test_foreflight_ahrs_deserialize_invalid_heading():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=None,
        is_magnetic_heading=None,
        indicated_airspeed=100,
        true_airspeed=120,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x01\xc2\x01\x2c\xff\xff\x00\x64\x00\x78\xc4\x5d\x7e"
    )


def test_foreflight_ahrs_serialize_invalid_indicated_airspeed():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=None,
        true_airspeed=120,
    )
    assert ffa.serialize(outgoing_lsb=False)[9:11] == b"\xff\xff"


def test_foreflight_id_deserialize_invalid_indicated_airspeed():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=None,
        true_airspeed=120,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x01\xc2\x01\x2c\x83\x20\xff\xff\x00\x78\x0b\x28\x7e"
    )


def test_foreflight_ahrs_serialize_invalid_true_airspeed():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=None,
    )
    assert ffa.serialize(outgoing_lsb=False)[11:13] == b"\xff\xff"


def test_foreflight_id_deserialize_invalid_true_airspeed():
    ffa = ForeFlightAHRSMessage(
        roll=45,
        pitch=30,
        heading=80,
        is_magnetic_heading=True,
        indicated_airspeed=100,
        true_airspeed=None,
    )
    assert ffa == ForeFlightAHRSMessage.deserialize(
        b"\x7e\x65\x01\x01\xc2\x01\x2c\x83\x20\x00\x64\xff\xff\xa1\xe6\x7e"
    )


def test_foreflight_ahrs_deserialize_too_long():
    with pytest.raises(DataTooLong):
        ForeFlightAHRSMessage.deserialize(
            b"\x7e\x65\x01\x01\xc2\x01\x2c\x83\x20\x00\x64\x00\x78\x00\x18\xa5\x7e"
        )

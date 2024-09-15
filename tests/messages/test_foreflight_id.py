import pytest

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.foreflight_id import ForeFlightIDMessage


def test_foreflight_id_serialize():
    ffid = ForeFlightIDMessage(
        device_serial_number=1234,
        device_name="TEST DEV",
        device_long_name="TEST DEVICE😎",
        is_msl=True,
    )
    assert (
        ffid.serialize(outgoing_lsb=False)
        == b"\x7e\x65\x00\x01\x00\x00\x00\x00\x00\x00\x04\xd2\x54\x45\x53\x54\x20\x44\x45\x56\x54\x45\x53\x54\x20\x44\x45\x56\x49\x43\x45\xf0\x9f\x98\x8e\x20\x01\x00\x00\x00\x33\xa5\x7e"
    )


def test_foreflight_id_deserialize():
    ffid = ForeFlightIDMessage(
        device_serial_number=1234,
        device_name="TEST DEV",
        device_long_name="TEST DEVICE😎",
        is_msl=True,
    )
    assert ffid == ForeFlightIDMessage.deserialize(
        b"\x7e\x65\x00\x01\x00\x00\x00\x00\x00\x00\x04\xd2\x54\x45\x53\x54\x20\x44\x45\x56\x54\x45\x53\x54\x20\x44\x45\x56\x49\x43\x45\xf0\x9f\x98\x8e\x20\x01\x00\x00\x00\x33\xa5\x7e"
    )


def test_foreflight_id_serialize_invalid_serial():
    ffid = ForeFlightIDMessage(
        device_serial_number=None,
        device_name="TEST DEV",
        device_long_name="TEST DEVICE😎",
        is_msl=True,
    )
    assert (
        ffid.serialize(outgoing_lsb=False)[4:12] == b"\xff\xff\xff\xff\xff\xff\xff\xff"
    )


def test_foreflight_id_deserialize_invalid_serial():
    ffid = ForeFlightIDMessage(
        device_serial_number=None,
        device_name="TEST DEV",
        device_long_name="TEST DEVICE😎",
        is_msl=True,
    )
    assert ffid == ForeFlightIDMessage.deserialize(
        b"\x7e\x65\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\x54\x45\x53\x54\x20\x44\x45\x56\x54\x45\x53\x54\x20\x44\x45\x56\x49\x43\x45\xf0\x9f\x98\x8e\x20\x01\x00\x00\x00\xaf\x9e\x7e"
    )


def test_foreflight_id_serialize_empty_long_name():
    ffid = ForeFlightIDMessage(
        device_serial_number=None,
        device_name="TEST DEV",
        device_long_name=None,
        is_msl=True,
    )
    assert (
        ffid.serialize(outgoing_lsb=False)[20:36]
        == b"TEST\x20DEV\x20\x20\x20\x20\x20\x20\x20\x20"
    )


def test_foreflight_id_deserialize_too_long():
    with pytest.raises(DataTooLong):
        ForeFlightIDMessage.deserialize(
            b"\x7e\x65\x00\x01\x00\x00\x00\x00\x00\x00\x04\xd2\x54\x45\x53\x54\x20\x44\x45\x56\x54\x45\x53\x54\x20\x44\x45\x56\x49\x43\x45\xf0\x9f\x98\x8e\x20\x01\x00\x00\x00\x00\x4f\xd6\x7e"
        )

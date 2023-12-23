import pytest

from gdl90py.exceptions import DataTooLong, UplinkDataWrongSize
from gdl90py.messages.uplink_data import UplinkDataMessage

TEST_UPLINK_DATA = b"\x00" * 432


def test_uplink_data_serialize():
    upd = UplinkDataMessage(
        time_of_reception=50000000,
        uplink_payload=TEST_UPLINK_DATA,
    )
    assert (
        upd.serialize(outgoing_lsb=False)
        == b"\x7e\x07\x68\x89\x09" + TEST_UPLINK_DATA + b"\x07\xc6\x7e"
    )


def test_uplink_data_deserialize():
    upd = UplinkDataMessage(
        time_of_reception=50000000,
        uplink_payload=TEST_UPLINK_DATA,
    )
    assert upd == UplinkDataMessage.deserialize(
        b"\x7e\x07\x68\x89\x09" + TEST_UPLINK_DATA + b"\x07\xc6\x7e"
    )


def test_uplink_data_invalid_tor_serialize():
    upd = UplinkDataMessage(
        time_of_reception=100000001,
        uplink_payload=TEST_UPLINK_DATA,
    )
    assert upd.serialize(outgoing_lsb=False)[2:5] == b"\xff\xff\xff"


def test_uplink_data_invalid_tor_deserialize():
    upd = UplinkDataMessage(
        time_of_reception=None,
        uplink_payload=TEST_UPLINK_DATA,
    )
    assert upd == UplinkDataMessage.deserialize(
        b"\x7e\x07\xff\xff\xff" + TEST_UPLINK_DATA + b"\xae\xbb\x7e"
    )


def test_uplink_data_deserialize_too_long():
    with pytest.raises(DataTooLong):
        UplinkDataMessage.deserialize(
            b"\x7e\x07\x68\x89\x09" + TEST_UPLINK_DATA + b"\x00\x8a\xbe\x7e"
        )


def test_uplink_data_wrong_size():
    upd = UplinkDataMessage(
        time_of_reception=None,
        uplink_payload=TEST_UPLINK_DATA + b"\x00",
    )
    with pytest.raises(UplinkDataWrongSize):
        upd.serialize()

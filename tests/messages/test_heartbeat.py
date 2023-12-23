import datetime

import pytest

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.heartbeat import HeartbeatMessage


def test_message_count_serialize():
    hb = HeartbeatMessage(
        gps_position_valid=False,
        maintenance_required=False,
        ident_talkback=False,
        self_assigned_address_talkback=False,
        gps_battery_low=False,
        RATCS_talkback=False,
        UAT_initialized=False,
        CSA_requested=False,
        CSA_unavailable=False,
        UTC_timing_valid=False,
        timestamp=datetime.datetime.now().time(),
        uplink_messages_count=4,
        basic_long_messages_count=567,
    )
    data = hb.serialize(outgoing_lsb=False)
    assert data[6] == 0x22
    assert data[7] == 0x37


def test_heartbeat_serialize():
    hb = HeartbeatMessage(
        gps_position_valid=True,
        maintenance_required=False,
        ident_talkback=True,
        self_assigned_address_talkback=False,
        gps_battery_low=True,
        RATCS_talkback=False,
        UAT_initialized=True,
        CSA_requested=False,
        CSA_unavailable=True,
        UTC_timing_valid=False,
        timestamp=datetime.time(
            hour=4, minute=20, second=0, tzinfo=datetime.timezone.utc
        ),
        uplink_messages_count=234,
        basic_long_messages_count=678,
    )
    assert (
        hb.serialize(outgoing_lsb=False)
        == b"\x7e\x00\xa9\x20\xf0\x3c\xfa\xa6\x7f\x81\x7e"
    )


def test_heartbeat_deserialize():
    hb = HeartbeatMessage(
        gps_position_valid=True,
        maintenance_required=False,
        ident_talkback=True,
        self_assigned_address_talkback=False,
        gps_battery_low=True,
        RATCS_talkback=False,
        UAT_initialized=True,
        CSA_requested=False,
        CSA_unavailable=True,
        UTC_timing_valid=False,
        timestamp=datetime.time(
            hour=4, minute=20, second=0, tzinfo=datetime.timezone.utc
        ),
        uplink_messages_count=31,  # 5-bit integer limit
        basic_long_messages_count=678,
    )
    assert hb == HeartbeatMessage.deserialize(
        b"\x7e\x00\xa9\x20\xf0\x3c\xfa\xa6\x7f\x81\x7e"
    )


def test_heartbeat_deserialize_too_long():
    with pytest.raises(DataTooLong):
        HeartbeatMessage.deserialize(
            b"\x7e\x00\xa9\x20\xf0\x3c\xfa\xa6\x00\xa9\xfe\x7e"
        )
